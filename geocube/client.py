from __future__ import annotations

import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Union, Optional

import grpc
import numpy as np
import parse
import rasterio
from shapely import geometry

from geocube.pb import records_pb2, operations_pb2, catalog_pb2, layouts_pb2, \
    geocube_pb2_grpc as geocube_grpc, variables_pb2, version_pb2
from geocube import entities, utils, Downloader

FileFormatRaw = catalog_pb2.Raw
FileFormatGTiff = catalog_pb2.GTiff


class Client:
    def __init__(self, uri: str, secure: bool = False, api_key: str = "", verbose: bool = True):
        """
        Initialise the connexion to the Geocube Server

        Args:
            uri: of the Geocube Server
            secure: True to use a TLS Connexion
            api_key: (optional) API Key if Geocube Server is secured using a bearer authentication
            verbose: set the default verbose mode
        """
        if secure:
            credentials = grpc.ssl_channel_credentials()
            if api_key != "":
                token_credentials = grpc.access_token_call_credentials(api_key)
                credentials = grpc.composite_channel_credentials(credentials, token_credentials)
            self._channel = grpc.secure_channel(uri, credentials)
        else:
            self._channel = grpc.insecure_channel(uri)
        self.stub = geocube_grpc.GeocubeStub(self._channel)
        self.verbose = verbose
        if verbose:
            print("Connected to Geocube v" + self.version())
        self.downloader = None

    def use_downloader(self, downloader: Downloader):
        self.downloader = downloader

    @utils.catch_rpc_error
    def version(self) -> str:
        """ Returns the version of the Geocube Server """
        return self.stub.Version(version_pb2.GetVersionRequest()).Version

    @utils.catch_rpc_error
    def variable(self, name: str = None, id_: str = None, instance_id: str = None)\
            -> Union[entities.Variable, entities.VariableInstance]:
        """
        Fetch a variable given an id, a name or an instance id (mutually exclusive)

        Args:
            name:
            id_: internal id of the variable (uuid4)
            instance_id: internal id of one instance of the variable (uuid4)

        Returns:
            either a Variable (first two cases) or a VariableInstance (specialization of the variable)
        """
        if id_:
            req = variables_pb2.GetVariableRequest(id=id_)
        elif name:
            req = variables_pb2.GetVariableRequest(name=name)
        elif instance_id:
            req = variables_pb2.GetVariableRequest(instance_id=instance_id)
        else:
            raise ValueError("One of id_, name or instance_id must be defined")

        resp = self.stub.GetVariable(req)
        v = entities.Variable.from_pb(self.stub, resp.variable)
        for i in v.instances.values():
            if i.id == instance_id:
                return v.instance(i.name)
        return v

    @utils.catch_rpc_error
    def create_variable(self, name: str, dformat: entities.DataFormat, bands: List[str], unit: str = "",
                        description: str = "", palette: str = "",
                        resampling_alg: entities.Resampling = entities.Resampling.bilinear, exist_ok: bool = False)\
            -> entities.Variable:
        """ Create a single Variable

        Args:
            name: Name of the variable
            dformat: data format of the variable (min and max are the theoretical extrema)
            bands: Name of the bands
            unit: of the data (for user information only)
            description: of the data (for user information only)
            palette: for rendering in png (TileServer). Must be created using create_palette.
            resampling_alg: when reprojection is needed (see entities.Resampling)
            exist_ok: (optional, see warning): if already exists, do not raise an error. !!! WARNING: it does not mean
                that the variable already stored in the geocube is exactly the same !!!

        Returns:
            the variable
        """
        req = variables_pb2.CreateVariableRequest(variable=variables_pb2.Variable(
            name=name,
            unit=unit,
            description=description,
            dformat=entities.DataFormat.from_user(dformat).to_pb(),
            bands=bands,
            palette=palette,
            resampling_alg=resampling_alg.value-1))

        try:
            return self.variable(id_=self.stub.CreateVariable(req).id)
        except grpc.RpcError as e:
            e = utils.GeocubeError.from_rpc(e)
            if e.is_already_exists() and exist_ok:
                return self.variable(name)
            raise

    @utils.catch_rpc_error
    def create_palette(self, name: str, colors: List[Tuple[float, int, int, int, int]], replace: bool = False):
        """
        Create a new palette from [0, 1] to RGBA, providing a list of index from 0 to 1.
        The intermediate values are linearly interpolated.

        Args:
            name: Name of the palette
            colors: a list of tuple[index, R, G, B, A] mapping index to the corresponding RGBA value
            replace: if a palette already exists with the same name, replace it else raise an error.
        """
        colors = [variables_pb2.colorPoint(value=v[0], r=v[1], g=v[2], b=v[3], a=v[4]) for v in colors]
        req = variables_pb2.CreatePaletteRequest(palette=variables_pb2.Palette(name=name, colors=colors),
                                                 replace=replace)
        self.stub.CreatePalette(req)

    @utils.catch_rpc_error
    def list_variables(self, name: str = "", limit: int = 0, page: int = 0) -> List[entities.Variable]:
        """
        List all the variables given a pattern

        Args:
            name: pattern of the name. * and ? are supported to match all or any character.
                (?i) can be added at the end to be insensitive to case
            limit: limit the number of variables returned
            page: number of the page (starting at 0).

        Returns:
            a list of variable
        """
        req = variables_pb2.ListVariablesRequest(name=name, limit=limit, page=page)
        return [entities.Variable.from_pb(self.stub, resp.variable) for resp in self.stub.ListVariables(req)]

    @utils.catch_rpc_error
    def create_aoi(self, aoi: Union[geometry.Polygon, geometry.MultiPolygon], exist_ok: bool = False) -> str:
        """
        Create a new AOI. Raise an error if an AOI with the same coordinates already exists.
        The id of the AOI can be retrieved from the details of the error.

        Args:
            aoi: in geographic coordinates
            exist_ok: (optional): if already exists, do not raise an error and return the aoi_id

        Returns:
            the id of the AOI
        """
        try:
            req = records_pb2.CreateAOIRequest(aoi=entities.aoi_to_pb(aoi))
            return self.stub.CreateAOI(req).id
        except grpc.RpcError as e:
            e = utils.GeocubeError.from_rpc(e)
            if e.is_already_exists() and exist_ok:
                return e.details[e.details.rindex(' ') + 1:]
            raise

    def create_record(self, aoi_id: str, name: str, tags: Dict[str, str], date: datetime, exist_ok: bool = False)\
            -> str:
        """
        Create a new record. A record is uniquely identified with the tuple (name, tags, date)
        Raise an error if a record with the same Name, Tags and Date already exists.

        Args:
            aoi_id: uuid4 of the AOI.
            name: of the records.
            tags: user-defined tags associated to the record.
            date: date of the data referenced by the record.
            exist_ok: (optional, see warning): if already exists, do not raise an error !!! WARNING: it does not mean
                that the record in the geocube is the same: its aoi may be different !!!

        Returns:
            the ID of the record
        """
        try:
            return self.create_records([aoi_id], [name], [tags], [date])[0]
        except utils.GeocubeError as e:
            if e.is_already_exists() and exist_ok:
                record = self.list_records(name, tags=tags, from_time=date, to_time=date)[0]
                if record.aoi_id != aoi_id:
                    warnings.warn("Record already exists in the Geocube but the aoi_id is different")
                return record.id
            raise

    @utils.catch_rpc_error
    def create_records(self, aoi_ids: List[str], names: List[str],
                       tags: List[Dict[str, str]], dates: List[datetime]) -> List[str]:
        """
        Create a list of records. All inputs must have the same length.
        (see create_record for the description of the parameters)
        """
        if len(names) != len(aoi_ids) or len(names) != len(dates) or len(names) != len(tags):
            raise ValueError("All fields must have the same length")

        records = []
        for i in range(len(names)):
            record = records_pb2.NewRecord(aoi_id=aoi_ids[i], name=names[i], tags=tags[i])
            record.time.FromDatetime(dates[i])
            records.append(record)

        req = records_pb2.CreateRecordsRequest(records=records)
        return self.stub.CreateRecords(req).ids

    @utils.catch_rpc_error
    def list_records(self, name: str = "", tags: Dict[str, str] = None,
                     from_time: datetime = None, to_time: datetime = None,
                     aoi: geometry.MultiPolygon = None,
                     limit: int = 10000, page: int = 0, with_aoi: bool = False) -> List[entities.Record]:
        """
        List records given filters

        Args:
            name: pattern of the name. * and ? are supported to match all or any character.
                (?i) can be added at the end to be insensitive to case
            tags: list of mandatory tags. Support the same pattern as name.
            from_time: filter by date
            to_time: filter by date
            aoi: records that intersect the AOI in geographic coordinates
            limit: the number of records returned (0 to return all records)
            page: start at 0
            with_aoi: also returns the AOI of the record. Otherwise, only the ID of the aoi is returned.
                load_aoi(record) can be called to retrieve the AOI later.

        Returns:
            a list of records
        """
        req = records_pb2.ListRecordsRequest(name=name, tags=tags,
                                             aoi=entities.aoi_to_pb(aoi),
                                             limit=limit, page=page, with_aoi=with_aoi)

        if from_time is not None:
            req.from_time.FromDatetime(from_time)
        if to_time is not None:
            req.to_time.FromDatetime(to_time)

        records = [entities.Record.from_pb(resp.record) for resp in self.stub.ListRecords(req)]
        if limit != 0 and len(records) == limit:
            warnings.warn("Maximum number of records reached. Call list_records(..., page=) or "
                          "list_records(..., limit=) to get more records.")

        return records

    @utils.catch_rpc_error
    def load_aoi(self, aoi_id: Union[str, entities.Record]) -> geometry.MultiPolygon:
        """
        Load the geometry of the AOI of the given record

        Args:
            aoi_id: uuid of the AOI or the record. If the record is provided, its geometry will be updated

        Returns:
            the geometry of the AOI
        """
        record = None
        if isinstance(aoi_id, entities.Record):
            record = aoi_id
            aoi_id = record.aoi_id
        resp = self.stub.GetAOI(records_pb2.GetAOIRequest(id=aoi_id))
        aoi = entities.aoi_from_pb(resp.aoi)
        if record:
            record.aoi = aoi
        return aoi

    @utils.catch_rpc_error
    def add_records_tags(self, records: List[Union[str, entities.Record]], tags: Dict[str, str]) -> int:
        """ Add or update tags to a list of records

        Args:
            records: List of records to be updated
            tags: List of new tags or tags to be updated

        Returns:
            the number of updated records
        """
        req = records_pb2.AddRecordsTagsRequest(ids=entities.get_ids(records), tags=tags)
        return self.stub.AddRecordsTags(req).nb

    @utils.catch_rpc_error
    def remove_records_tags(self, records: List[Union[str, entities.Record]], tag_keys: List[str]) -> int:
        """ Remove tags keys from a list of records

        Args:
            records: List of records to be updated
            tag_keys: List of keys to be deleted

        Returns:
            the number of updated records
        """
        req = records_pb2.RemoveRecordsTagsRequest(ids=entities.get_ids(records), tagsKey=tag_keys)
        return self.stub.RemoveRecordsTags(req).nb

    @utils.catch_rpc_error
    def delete_records(self, records: List[Union[str, entities.Record]]):
        """
        Delete records iif no dataset are indexed to them.

        Args:
            records: List of records to be deleted
        """
        req = records_pb2.DeleteRecordsRequest(ids=entities.get_ids(records))
        self.stub.DeleteRecords(req)

    @utils.catch_rpc_error
    def index(self, containers: List[entities.Container]):
        """
        Index a new container.

        Args:
            containers: List of container to index.
        """
        pb_containers = []
        for container in containers:

            datasets = [dataset.to_pb() for dataset in container.datasets]

            pb_containers.append(operations_pb2.Container(
                uri=container.uri,
                managed=container.managed,
                datasets=datasets
            ))

        for c in pb_containers:
            req = operations_pb2.IndexDatasetsRequest(container=c)
            self.stub.IndexDatasets(req)

    @utils.catch_rpc_error
    def index_dataset(self, uri: str, record: Union[str, entities.Record, Tuple[str, Dict[str, str], datetime]],
                      instance: entities.VariableInstance, dformat: entities.DataFormat, bands: List[int] = None,
                      min_out: float = None, max_out: float = None, exponent: float = 1):
        """
        Index the given "bands" of the dataset located at "uri", referenced by a record and an instance.

        Args:
            uri: of the file to index
            record: id of the record describing the data-take or a tuple (name, metadata, datetime)
                to create the record on the fly
            instance: describing the data
            dformat: describing the internal format (see entities.DataFormat.from_user())
            bands: subset of bands' file (start at 1) that maps to `variable.bands` (by default, all the bands)
            min_out: (optional, default: instance.dformat.min_value, instance.dformat.dtype) maps dformat.min_value
            max_out: (optional, default: instance.dformat.max_value, instance.dformat.dtype) maps dformat.max_value
            exponent: (optional, default: 1) non-linear scaling between dformat.min_max_value to min_max_out.
        """
        ds_dtype = "u1"
        if isinstance(record, tuple) or dformat is None:
            try:
                with rasterio.open(uri) as ds:
                    tile = entities.Tile.from_geotransform(ds.transform, ds.crs, ds.shape)
                    ds_dtype = ds.dtypes[0]
            except Exception as e:
                raise f'if "record" is a tuple or "bands" or "dformat" is not defined, geocube-client tries to deduce'\
                      f'some information reading the file {uri}, but it encountered the following error :{e}.'

        if isinstance(record, tuple):
            aoi_id = self.create_aoi(tile.geometry(4326), exist_ok=True)

            r_name, r_tags, r_date = record
            record = self.create_record(aoi_id, name=r_name, tags=r_tags, date=r_date, exist_ok=True)

        if dformat is None:
            dformat = entities.DataFormat.from_user(ds_dtype)

        cs = [entities.Container(uri,
                                 managed=False,
                                 datasets=[entities.Dataset(record, instance, bands=bands,
                                                            dformat=entities.DataFormat.from_user(dformat),
                                                            min_out=min_out, max_out=max_out, exponent=exponent)])]
        return self.index(cs)

    def get_cube_metadata(self, params: entities.CubeParams) -> entities.CubeMetadata:
        cube_it = self._get_cube_it(params, headers_only=True)
        return cube_it.metadata()

    @utils.catch_rpc_error
    def get_cube(self, params: entities.CubeParams,
                 headers_only: bool = False, compression: int = 0, verbose: bool = None) \
            -> Tuple[List[np.array], List[entities.GroupedRecords]]:
        """ Get a cube given a CubeParameters

        Args:
            params: CubeParams (see entities.CubeParams)
            headers_only: Only returns the header of each image (gives an overview of the query)
            compression: define a level of compression to speed up the transfer.
                (0: no compression, 1 fastest to 9 best, -2: huffman-only)
                The data is compressed by the server and decompressed by the Client.
                Compression=0 or -2 is advised if the bandwidth is not limited
            verbose: display information during the transfer (if None, use the default verbose mode)

        Returns:
            list of images (np.ndarray) and the list of corresponding records
                (several records can be returned for each image when they are grouped together,
                by date or something else. See entities.Record.group_by)
        """
        cube = self._get_cube_it(params, headers_only=headers_only, compression=compression)
        images, grouped_records = [], []
        verbose = self.verbose if verbose is None else verbose
        if verbose:
            print("GetCube returns {} images from {} datasets".format(cube.count, cube.nb_datasets))
        for image, metadata, err in cube:
            if err is not None:
                if verbose:
                    print(err)
                continue
            if verbose:
                min_date = metadata.min_date.strftime("%Y-%m-%d_%H:%M:%S")
                max_date = metadata.max_date.strftime("%Y-%m-%d_%H:%M:%S")
                print("Image {} received ({}{}kb) RecordTime:{} RecordName:{} Shape:{}".format(
                    cube.index+1, '<' if headers_only else '', metadata.bytes//1024,
                    min_date if min_date == max_date else min_date + " to " + max_date,
                    metadata.grouped_records[0].name, image.shape))
            images.append(image)
            grouped_records.append(metadata.grouped_records)

        return images, grouped_records

    @utils.catch_rpc_error
    def get_cube_it(self, params: entities.CubeParams, headers_only: bool = False, compression: int = 0,
                    file_format=FileFormatRaw, file_pattern: str = None) -> entities.CubeIterator:
        """ Returns a cube iterator over the requested images

        Args:
            params: CubeParams (see entities.CubeParams)

            headers_only : returns only the header of the dataset (use this option to control the output of get_cube)
            compression : define a level of compression to speed up the transfer
                (0: no compression, 1 fastest to 9 best, -2: huffman-only)
                The data is compressed by the server and decompressed by the Client.
                Compression=0 or -2 is advised if the bandwidth is not limited
            file_format : (optional) currently supported geocube.FileFormatRaw & geocube.FileFormatGTiff
            file_pattern : (optional) iif file_format != Raw, pattern of the file name.
                {#} will be replaced by the number of image, {date} and {id} by the value of the record

        Returns:
            an iterator yielding an image, its associated records, an error (or None) and the size of the image
        >>> client = Client('127.0.0.1:8080', False)
        >>> cube_params = entities.CubeParams.from_records("+proj=utm +zone=31",
        ...     entities.geo_transform(366162, 4833123, 30), (512, 512),
        ...     client.variable(name="test/rgb").instance("master"), records=client.list_records('france'))
        affine.Affine.translation(366162, 4833123)*affine.Affine.scale(30, -30))
        >>> cube_it = client._get_cube_it(cube_params)
        >>> from matplotlib import pyplot as plt
        >>> for image, _, _, err in cube_it:
        ...     if not err:
        ...         plt.figure(cube_it.index+1)
        ...         plt.imshow(image)
        """
        return self._get_cube_it(params, headers_only, compression, file_format, file_pattern)

    def _get_cube_it(self, params: entities.CubeParams, headers_only: bool = False, compression: int = 1,
                     file_format=FileFormatRaw, file_pattern: str = None) -> entities.CubeIterator:
        if self.downloader is not None and not headers_only:
            metadata = self._get_cube_it(params, headers_only=True).metadata()
            return self.downloader.get_cube_it(metadata, file_format, file_pattern)

        common = {
            "instances_id":      [params.instance],
            "crs":               params.crs,
            "pix_to_crs":        layouts_pb2.GeoTransform(
                a=params.transform.c, b=params.transform.a, c=params.transform.b,
                d=params.transform.f, e=params.transform.d, f=params.transform.e),
            "size":              layouts_pb2.Size(width=params.shape[0], height=params.shape[1]),
            "compression_level": compression,
            "headers_only":      headers_only,
            "format":            file_format,
        }
        if params.records is not None:
            req = catalog_pb2.GetCubeRequest(**common, grouped_records=records_pb2.GroupedRecordIdsList(
                records=[records_pb2.GroupedRecordIds(ids=rs) for rs in params.records]
            ))
        else:
            from_time_pb = utils.pb_null_timestamp()
            if params.from_time is not None:
                from_time_pb.FromDatetime(params.from_time)
            to_time_pb = utils.pb_null_timestamp()
            if params.to_time is not None:
                to_time_pb.FromDatetime(params.to_time)
            req = catalog_pb2.GetCubeRequest(**common, filters=records_pb2.RecordFilters(
                tags=params.tags, from_time=from_time_pb, to_time=to_time_pb
            ))
        return entities.CubeIterator(self.stub.GetCube(req), file_format, file_pattern)

    @utils.catch_rpc_error
    def tile_aoi(self, aoi: geometry.MultiPolygon,
                 layout_name: Optional[str] = None,
                 layout: Optional[entities.Layout] = None,
                 resolution: Optional[float] = None,
                 crs: Optional[str] = None, shape: Optional[Tuple[int, int]] = None) -> List[entities.Tile]:
        """
        Tile an AOI

        Args:
            aoi: AOI to be tiled in **geographic coordinates**
            crs: CRS of the tile (not the AOI)
            resolution: resolution of the tile
            shape: shape of each tile
            layout_name: use a defined layout.
            layout: use a customer defined layout

        Returns:
            a list of Tiles covering the AOI in the given CRS at the given resolution
        """
        aoi = entities.aoi_to_pb(aoi)
        if layout_name is not None:
            req = layouts_pb2.TileAOIRequest(aoi=aoi, layout_name=layout_name)
        else:
            if layout is None:
                layout = entities.Layout.regular("", crs, shape, resolution)
            req = layouts_pb2.TileAOIRequest(aoi=aoi, layout=layout.to_pb())

        return [entities.Tile.from_pb(tile) for resp in self.stub.TileAOI(req) for tile in resp.tiles]

    @utils.catch_rpc_error
    def get_xyz_tile(self, instance: Union[str, entities.VariableInstance],
                     records: List[Union[str, entities.Record]], x: int, y: int, z: int, file: str):
        """
        Create a PNG file covering the (X,Y,Z) web-mercator tile, using the palette of the variable.

        Args:
            instance: instance of the variable
            records: list of records
            x: coordinate of the web-mercator XYZ tile
            y: coordinate of the web-mercator XYZ tile
            z: coordinate of the web-mercator XYZ tile
            file: output PNG file
        """
        req = catalog_pb2.GetTileRequest(
            records=records_pb2.RecordIdList(ids=entities.get_ids(records)),
            instance_id=entities.get_id(instance),
            x=x, y=y, z=z)
        resp = self.stub.GetXYZTile(req)
        f = open(file, "wb")
        f.write(resp.image.data)
        f.close()

    @utils.catch_rpc_error
    def create_layout(self, layout: entities.Layout, exist_ok=False):
        """ Create a layout in the Geocube
        exist_ok: (optional, see warning): if already exists, do not raise an error. !!! WARNING: it does not mean that
        the layout already stored in the geocube is exactly the same !!!
        """
        try:
            self.stub.CreateLayout(layouts_pb2.CreateLayoutRequest(layout=layout.to_pb()))
        except utils.GeocubeError as e:
            if not e.is_already_exists() or not exist_ok:
                raise

    @utils.catch_rpc_error
    def list_layouts(self, name_like: str = "") -> List[entities.Layout]:
        """
        List available layouts by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        res = self.stub.ListLayouts(layouts_pb2.ListLayoutsRequest(name_like=name_like))
        return [entities.Layout.from_pb(layout) for layout in res.layouts]

    @utils.catch_rpc_error
    def find_container_layouts(self, instance: Union[str, entities.VariableInstance],
                               records: List[Union[str, entities.Record]] = None,
                               tags: Dict[str, str] = None,
                               from_time: datetime = None, to_time: datetime = None,
                               aoi: geometry.MultiPolygon = None) -> Dict[str, List[str]]:
        """
        Find layouts of the containers covering an area or a list of records for a given instance
        """
        if records is not None:
            req = layouts_pb2.FindContainerLayoutsRequest(
                instance_id=entities.get_id(instance),
                records=records_pb2.RecordIdList(ids=entities.get_ids(records))
            )
        else:
            from_time_pb = utils.pb_null_timestamp()
            if from_time is not None:
                from_time_pb.FromDatetime(from_time)
            to_time_pb = utils.pb_null_timestamp()
            if to_time is not None:
                to_time_pb.FromDatetime(to_time)
            req = catalog_pb2.GetCubeRequest(
                instance_id=entities.get_id(instance),
                filters=records_pb2.RecordFiltersWithAOI(aoi=aoi, tags=tags,
                                                         from_time=from_time_pb, to_time=to_time_pb))
        return {resp.layout_name: resp.container_uris for resp in self.stub.FindContainerLayouts(req)}

    @utils.catch_rpc_error
    def delete_layout(self, name: str = ""):
        """ Delete a layout from the Geocube """
        self.stub.DeleteLayout(layouts_pb2.DeleteLayoutRequest(name=name))

    @utils.catch_rpc_error
    def create_grid(self, grid: entities.Grid):
        """ Create a grid in the Geocube"""
        max_cells = min(len(grid.cells), 10000000)
        while True:
            try:
                req = [layouts_pb2.CreateGridRequest(grid=grid.to_pb(max_cells*i, max_cells*(i+1)))
                       for i in range((len(grid.cells)-1)//max_cells+1)]
                return self.stub.CreateGrid(iter(req))
            except grpc.RpcError as e:
                e = utils.GeocubeError.from_rpc(e)
                if e.codename != "RESOURCE_EXHAUSTED":
                    raise
                r = parse.search("({volume:d} vs. {max:d})", e.details)
                max_cells //= max(r["volume"] // r["max"], 2)

    @utils.catch_rpc_error
    def list_grids(self, name_like: str = "") -> List[entities.Grid]:
        """
        List grids by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        res = self.stub.ListGrids(layouts_pb2.ListGridsRequest(name_like=name_like))
        return [entities.Grid.from_pb(grid) for grid in res.grids]

    @utils.catch_rpc_error
    def delete_grid(self, name: str = ""):
        """ Delete a grid by its name """
        self.stub.DeleteGrid(layouts_pb2.DeleteGridRequest(name=name))
