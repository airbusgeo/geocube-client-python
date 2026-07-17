from __future__ import annotations

import os
import time
import typing
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Union, Optional

import grpc
import numpy as np
import parse
import rasterio
from tqdm import tqdm

from geocube.entities import cubeiterator
from shapely import geometry

from geocube.pb import records_pb2, operations_pb2, catalog_pb2, layouts_pb2, \
    geocube_pb2_grpc as geocube_grpc, variables_pb2, version_pb2
from geocube import entities, utils, Downloader
from geocube.stub import Stub

FileFormatRaw = catalog_pb2.Raw
FileFormatGTiff = catalog_pb2.GTiff

class Client:
    def __init__(self, uri: str, secure: bool = False, api_key: str = "", verbose: bool = True,
                 root_certificates: Optional[bytes] = None, ssl_target_name_override: Optional[str] = None):
        """
        Initialise the connexion to the Geocube Server

        Args:
            uri: of the Geocube Server
            secure: True to use a TLS Connexion
            api_key: (optional) API Key if Geocube Server is secured using bearer authentication
            verbose: set the default verbose mode
            root_certificates: (optional) PEM-encoded root certificates for server authentication.
                This is needed if the server uses a self-signed certificate.
            ssl_target_name_override: (optional) Used to override the server name for SSL verification.
                This is useful in cases where the server's certificate does not match the hostname.
        """
        assert uri is not None and uri != "", "geocube.Client: Cannot connect: uri is not defined"
        self.pid = os.getpid()
        if secure:
            # Start with SSL credentials. If root_certificates is None, system CAs are used.
            channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates)

            # If an API key is provided, combine it with the SSL credentials.
            if api_key != "":
                token_credentials = grpc.access_token_call_credentials(api_key)
                channel_credentials = grpc.composite_channel_credentials(channel_credentials, token_credentials)

            # Prepare channel options, like overriding the SSL target name for verification.
            options = []
            if ssl_target_name_override:
                options.append(('grpc.ssl_target_name_override', ssl_target_name_override))

            self._channel = grpc.secure_channel(uri, channel_credentials, options=options)
        else:
            self._channel = grpc.insecure_channel(uri)
            if root_certificates is not None:
                warnings.warn("`root_certificates` is provided, but `secure` is False. The certificate will be ignored.")
            if ssl_target_name_override is not None:
                warnings.warn("`ssl_target_name_override` is provided, but `secure` is False. The override will be ignored.")

        self.stub = Stub(geocube_grpc.GeocubeStub(self._channel))
        self.verbose = verbose
        if verbose:
            print("Connected to Geocube v" + self.version())
        self.downloader = None

    def is_pid_ok(self) -> bool:
        return self.pid == os.getpid()

    def use_downloader(self, downloader: Downloader):
        self.downloader = downloader

    def set_timeout(self, timeout_sec: float):
        self.stub.timeout = timeout_sec

    def version(self) -> str:
        """ Returns the version of the Geocube Server """
        return self._version()

    def variable(self, name: str = None, id_: str = None, instance_id: str = None) \
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
        return self._variable(name, id_, instance_id)

    def create_variable(self, name: str, dformat: entities.DataFormat, bands: List[str], unit: str = "",
                        description: str = "", palette: str = "",
                        resampling_alg: entities.Resampling = entities.Resampling.bilinear, exist_ok: bool = False) \
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
        return self._create_variable(name, dformat, bands, unit, description, palette, resampling_alg, exist_ok)

    def create_palette(self, name: str, colors: List[Tuple[float, int, int, int, int]], replace: bool = False):
        """
        Create a new palette from [0, 1] to RGBA, providing a list of index from 0 to 1.
        The intermediate values are linearly interpolated.

        Args:
            name: Name of the palette
            colors: a list of tuple[index, R, G, B, A] mapping index to the corresponding RGBA value
            replace: if a palette already exists with the same name, replace it else raise an error.
        """
        return self._create_palette(name, colors, replace)

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
        return self._list_variables(name, limit, page)

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
        return self._create_aoi(aoi, exist_ok)

    def create_record(self, aoi_id: str, name: str, tags: Dict[str, str], date: datetime, exist_ok: bool = False) \
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

    def create_records(self, aoi_ids: List[str], names: List[str],
                       tags: List[Dict[str, str]], dates: List[datetime]) -> List[str]:
        """
        Create a list of records. All inputs must have the same length.
        (see create_record for the description of the parameters)
        """
        return self._create_records(aoi_ids, names, tags, dates)

    def get_record(self, _id: str) -> entities.Record:
        """ Deprecated: use record() instead """
        return self.record(_id)

    def record(self, _id: str) -> entities.Record:
        """ Get a record by id """
        r = self.get_records([_id])
        assert len(r) > 0, utils.GeocubeError("get_record", grpc.StatusCode.NOT_FOUND.name, "record with id " + _id)
        return r[0]

    def get_records(self, ids: List[str]) -> List[entities.Record]:
        """
        Get a list of records.
        """
        return self._get_records(ids)

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
        return self._list_records(name, tags, from_time, to_time, aoi, limit, page, with_aoi)

    def load_aoi(self, aoi_id: Union[str, entities.Record]) -> geometry.MultiPolygon:
        """
        Load the geometry of the AOI of the given record

        Args:
            aoi_id: uuid of the AOI or the record. If the record is provided, its geometry will be updated

        Returns:
            the geometry of the AOI
        """
        return self._load_aoi(aoi_id)

    def add_records_tags(self, records: List[Union[str, entities.Record]], tags: Dict[str, str]) -> int:
        """ Add or update tags to a list of records

        Args:
            records: List of records to be updated
            tags: List of new tags or tags to be updated

        Returns:
            the number of updated records
        """
        return self._add_records_tags(records, tags)

    def remove_records_tags(self, records: List[Union[str, entities.Record]], tag_keys: List[str]) -> int:
        """ Remove tags keys from a list of records

        Args:
            records: List of records to be updated
            tag_keys: List of keys to be deleted

        Returns:
            the number of updated records
        """
        return self._remove_records_tags(records, tag_keys)

    def delete_records(self, records: List[Union[str, entities.Record]], no_fail: bool = False):
        """
        Delete records iif no dataset are indexed to them.

        Args:
            records: List of records to be deleted
            no_fail: if true, do not fail if some records still have datasets that refer to them, and delete the others
        """
        return self._delete_records(records, no_fail)

    def containers(self, uris: Union[str, List[str]]) -> Union[entities.Container, List[entities.Container]]:
        """
        Get containers and their datasets by uris

        Args:
            uris: uri or list of uris
        """
        return self._containers(uris)

    def index(self, containers: List[entities.Container]):
        """
        Index a new container.

        Args:
            containers: List of container to index.
        """
        return self._index(containers)

    def index_dataset(self, uri: str, record: Union[str, entities.Record, Tuple[str, Dict[str, str], datetime]],
                      instance: entities.VariableInstance, dformat: entities.DataFormat, bands: List[int] = None,
                      min_out: float = None, max_out: float = None, exponent: float = 1, managed: bool = False):
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
            managed: if True, the geocube takes the ownership of the file, removing it if the dataset is removed
        """
        return self._index_dataset(uri, record, instance, dformat, bands, min_out, max_out, exponent, managed)

    def delete_datasets(self, instances: List[Union[str, entities.VariableInstance]],
                        records: List[Union[str, entities.Record]],
                        file_patterns: List[str] = None,
                        execution_level: entities.ExecutionLevel = entities.ExecutionLevel.STEP_BY_STEP_CRITICAL,
                        job_name: str = None, allow_empty_instances=False, allow_empty_records=False) \
            -> entities.Job:
        """
        Function to delete datasets that are referenced by a list of instances and a list of records.

        Args:
            instances: select all the datasets referenced by these instances.
            records: select all the datasets referenced by these records.
            file_patterns: select all the datasets with on of the given file patterns
                (support * and ? for all or any characters and trailing (?i) for case-insensitiveness)
            execution_level: see entities.ExecutionLevel.
            job_name: [optional] gives a name to the job, otherwise, a name will be automatically generated
            allow_empty_instances: [optional] allows instances to be empty.
                @warning It means that the job will delete all the instances for the given records.
            allow_empty_records: [optional] allows records to be empty.
                @warning It means that the job will delete all the records for the given instances.
        """
        return self._delete_datasets(instances, records, file_patterns,  execution_level,
                                     job_name, allow_empty_instances, allow_empty_records)

    def get_cube_metadata(self, params: entities.CubeParams) -> entities.CubeMetadata:
        return self._get_cube_metadata(params)

    def get_cube(self, params: entities.CubeParams, *,
                 resampling_alg: entities.Resampling = entities.Resampling.undefined,
                 headers_only: bool = False, compression: int = 0, verbose: bool = None) \
            -> Tuple[List[np.array], List[entities.GroupedRecords]]:
        """ Get a cube given a CubeParameters

        Args:
            params: CubeParams (see entities.CubeParams)
            resampling_alg: if defined, overwrite the variable.Resampling used for reprojection.
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
        cube = self._get_cube_it(params, resampling_alg=resampling_alg,
                                 headers_only=headers_only, compression=compression)
        images, grouped_records = [], []
        verbose = self.verbose if verbose is None else verbose
        if verbose:
            print("GetCube returns {} images from {} datasets".format(cube.count, cube.nb_datasets))
        for image, metadata, err in cube:
            if err is not None:
                if err == cubeiterator.NOT_FOUND_ERROR:
                    if verbose:
                        print(err)
                    continue
                raise ValueError(err)
            if verbose:
                min_date = metadata.min_date.strftime("%Y-%m-%d_%H:%M:%S")
                max_date = metadata.max_date.strftime("%Y-%m-%d_%H:%M:%S")
                print("Image {} received ({}{}kb) RecordTime:{} RecordName:{} Shape:{}".format(
                    cube.index + 1, '<' if headers_only else '', metadata.bytes // 1024,
                    min_date if min_date == max_date else min_date + " to " + max_date,
                    metadata.grouped_records[0].name, image.shape))
            images.append(image)
            grouped_records.append(metadata.grouped_records)

        return images, grouped_records

    def get_cube_it(self, params: entities.CubeParams, *,
                    resampling_alg: entities.Resampling = entities.Resampling.undefined,
                    headers_only: bool = False, compression: int = 0,
                    file_format=FileFormatRaw, file_pattern: str = None) -> entities.CubeIterator:
        """ Returns a cube iterator over the requested images

        Args:
            params: CubeParams (see entities.CubeParams)

            resampling_alg: if defined, overwrite the variable.Resampling used for reprojection.
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
        >>> cube_it = client.get_cube_it(cube_params)
        >>> from matplotlib import pyplot as plt
        >>> for image, _, _, err in cube_it:
        ...     if err != cubeiterator.NOT_FOUND_ERROR:
        ...         raise ValueError(err)
        ...     if not err:
        ...         plt.figure(cube_it.index+1)
        ...         plt.imshow(image)
        """
        return self._get_cube_it(params, resampling_alg=resampling_alg, headers_only=headers_only,
                                 compression=compression, file_format=file_format, file_pattern=file_pattern)

    def tile_aoi(self, aoi: Union[geometry.MultiPolygon, geometry.Polygon],
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
        return self._tile_aoi(aoi, layout_name, layout, resolution, crs, shape)

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
        return self._get_xyz_tile(instance, records, x, y, z, file)

    def create_layout(self, layout: entities.Layout, exist_ok=False):
        """ Create a layout in the Geocube
        exist_ok: (optional, see warning): if already exists, do not raise an error. !!! WARNING: it does not mean that
        the layout already stored in the geocube is exactly the same !!!
        """
        return self._create_layout(layout, exist_ok)

    def layout(self, name: str) -> entities.Layout:
        """
        Get layout by name
        """
        return self._layout(name)

    def list_layouts(self, name_like: str = "") -> List[entities.Layout]:
        """
        List available layouts by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        return self._list_layouts(name_like)

    def find_container_layouts(self, instance: Union[str, entities.VariableInstance],
                               records: List[Union[str, entities.Record]] = None,
                               tags: Dict[str, str] = None,
                               from_time: datetime = None, to_time: datetime = None,
                               aoi: geometry.MultiPolygon = None) -> Dict[str, List[str]]:
        """
        Find layouts of the containers covering an area or a list of records for a given instance
        """
        return self._find_container_layouts(instance, records, tags, from_time, to_time, aoi)

    def delete_layout(self, name: str = ""):
        """ Delete a layout from the Geocube """
        return self._delete_layout(name)

    def create_grid(self, grid: entities.Grid):
        """ Create a grid in the Geocube"""
        return self._create_grid(grid)

    def list_grids(self, name_like: str = "") -> List[entities.Grid]:
        """
        List grids by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        return self._list_grids(name_like)

    def delete_grid(self, name: str = ""):
        """ Delete a grid by its name """
        return self._delete_grid(name)

    def job(self, name: str = None, id_: str = None, log_page: int = 0, log_limit: int = 1000):
        """ Get job by name or by id
        name: if not None, shortcut for ListJobs(name)[0]. Only few logs are loaded.
        id_: if not None, get job by id. Logs are loaded by pages, because some big jobs have too many logs to fit in a gRPC response.
        log_page: pagination of the job's logs (starts at 0) (with id_ only, ignored otherwise)
        log_limit: number of job's logs returner (with id_ only, ignored otherwise)
        """
        if name is not None:
            return self._get_job_by_name(name)
        if id_ is not None:
            return self._get_job_by_id(id_, log_page, log_limit)
        raise ValueError("job: either name or id_ must be defined")

    def get_job(self, job_id: Union[str, entities.Job], log_page=0, log_limit=1000):
        """ Deprecated: use job() """
        return self.job(id_=job_id, log_page=log_page, log_limit=log_limit)

    def list_jobs(self, name_like: str = "", page=0, limit=10):
        """
        List jobs by name
        name_like: pattern of the name. * and ? are supported to match all or any character.
        """
        return self._list_jobs(name_like, page, limit)


    @staticmethod
    def wait_job(job: entities.Job, wait_secs=15, timeout_secs=None, verbose=True):
        """
        Wait for the job to finish or fail.
        If the execution level is step-by-step, it will automatically continue.
        If verbose=True, the last log is printed every time a state change is detected.
        """
        prev_state = job.state
        pbar = None
        while job.state not in ['DONE', 'FAILED', 'DONEBUTUNTIDY']:
            time.sleep(wait_secs)
            job.refresh(log_limit=1 if verbose else 0)
            if verbose:
                if job.active_tasks > 0 and pbar is None:
                    pbar = tqdm(total=job.active_tasks, desc="tasks")
                if pbar is not None and pbar.n != pbar.total - job.active_tasks:
                    pbar.update(pbar.total - job.active_tasks - pbar.n)
                if job.state != prev_state:
                    prev_state = job.state
                    print(job.logs[-1])
            if job.waiting:
                job.next()
            if timeout_secs is not None:
                timeout_secs -= wait_secs
                if timeout_secs < 0:
                    raise TimeoutError(f"job {job.name}: state={job.state}")

    def remove_terminated_jobs(self, name_like: str = "", state: str = ""):
        """
        Remove all the jobs from the Geocube given a name pattern (by default, all terminated jobs)
        name_like: pattern of the name. * and ? are supported to match all or any character.
        state: state of the jobs to be removed.
        """
        return self._remove_terminated_jobs(name_like, state)

    def consolidate(self,
                    job_name: str,
                    instance: Union[str, entities.VariableInstance],
                    layout: Union[str, entities.Layout],
                    *,
                    records: Union[List[entities.RecordIdentifiers], None] = None,
                    tags: Union[Dict[str, str], None] = None,
                    from_time: Union[datetime, None] = None,
                    to_time: Union[datetime, None] = None,
                    collapse_on_record: Union[entities.Record, str, None] = None,
                    execution_level: entities.ExecutionLevel = entities.ExecutionLevel.ASYNCHRONOUS):
        return self._consolidate(job_name, instance, layout, records, tags, from_time, to_time,
                                 collapse_on_record, execution_level)

    @utils.catch_rpc_error
    def _version(self) -> str:
        return self.stub.Version(version_pb2.GetVersionRequest()).Version

    @utils.catch_rpc_error
    def _variable(self, name: str, id_: str, instance_id: str) \
            -> Union[entities.Variable, entities.VariableInstance]:
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
    def _create_variable(self, name: str, dformat: entities.DataFormat, bands: List[str], unit: str,
                         description: str, palette: str, resampling_alg: entities.Resampling, exist_ok: bool) \
            -> entities.Variable:
        req = variables_pb2.CreateVariableRequest(variable=variables_pb2.Variable(
            name=name,
            unit=unit,
            description=description,
            dformat=entities.DataFormat.from_user(dformat).to_pb(),
            bands=bands,
            palette=palette,
            resampling_alg=typing.cast(int, resampling_alg.value) - 1))

        try:
            return self.variable(id_=self.stub.CreateVariable(req).id)
        except grpc.RpcError as e:
            e = utils.GeocubeError.from_rpc(e)
            if e.is_already_exists() and exist_ok:
                return self.variable(name)
            raise

    @utils.catch_rpc_error
    def _create_palette(self, name: str, colors: List[Tuple[float, int, int, int, int]], replace: bool):
        colors = [variables_pb2.colorPoint(value=v[0], r=v[1], g=v[2], b=v[3], a=v[4]) for v in colors]
        req = variables_pb2.CreatePaletteRequest(palette=variables_pb2.Palette(name=name, colors=colors),
                                                 replace=replace)
        self.stub.CreatePalette(req)

    @utils.catch_rpc_error
    def _list_variables(self, name: str, limit: int, page: int) -> List[entities.Variable]:
        req = variables_pb2.ListVariablesRequest(name=name, limit=limit, page=page)
        return [entities.Variable.from_pb(self.stub, resp.variable) for resp in self.stub.ListVariables(req)]

    @utils.catch_rpc_error
    def _create_aoi(self, aoi: Union[geometry.Polygon, geometry.MultiPolygon], exist_ok: bool) -> str:
        try:
            req = records_pb2.CreateAOIRequest(aoi=entities.aoi_to_pb(aoi))
            return self.stub.CreateAOI(req).id
        except grpc.RpcError as e:
            e = utils.GeocubeError.from_rpc(e)
            if e.is_already_exists() and exist_ok:
                return e.details[e.details.rindex(' ') + 1:]
            raise

    @utils.catch_rpc_error
    def _create_records(self, aoi_ids: List[str], names: List[str],
                        tags: List[Dict[str, str]], dates: List[datetime]) -> List[str]:

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
    def _get_records(self, ids: List[str]) -> List[entities.Record]:
        req = records_pb2.GetRecordsRequest(ids=ids)
        return [entities.Record.from_pb(resp.record) for resp in self.stub.GetRecords(req)]

    @utils.catch_rpc_error
    def _list_records(self, name: str, tags: Dict[str, str], from_time: datetime, to_time: datetime,
                      aoi: geometry.MultiPolygon, limit: int, page: int, with_aoi: bool) -> List[entities.Record]:
        req = records_pb2.ListRecordsRequest(name=name, tags=tags,
                                             aoi=entities.aoi_to_pb(aoi),
                                             limit=limit, page=page, with_aoi=with_aoi)

        if from_time is not None and to_time is not None and from_time >= to_time:
            message = f"Dates problem: from time ({from_time.isoformat()}) must be before to time ({to_time.isoformat()})"
            raise ValueError(message)
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
    def _load_aoi(self, aoi_id: Union[str, entities.Record]) -> geometry.MultiPolygon:
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
    def _add_records_tags(self, records: List[Union[str, entities.Record]], tags: Dict[str, str]) -> int:
        req = records_pb2.AddRecordsTagsRequest(ids=entities.get_ids(records), tags=tags)
        return self.stub.AddRecordsTags(req).nb

    @utils.catch_rpc_error
    def _remove_records_tags(self, records: List[Union[str, entities.Record]], tag_keys: List[str]) -> int:
        req = records_pb2.RemoveRecordsTagsRequest(ids=entities.get_ids(records), tagsKey=tag_keys)
        return self.stub.RemoveRecordsTags(req).nb

    @utils.catch_rpc_error
    def _delete_records(self, records: List[Union[str, entities.Record]], no_fail: bool):
        req = records_pb2.DeleteRecordsRequest(ids=entities.get_ids(records), no_fail=no_fail)
        self.stub.DeleteRecords(req)

    @utils.catch_rpc_error
    def _containers(self, uris: Union[str, List[str]]) -> Union[entities.Container, List[entities.Container]]:
        singleton = isinstance(uris, str)
        if singleton:
            uris = [uris]
        req = operations_pb2.GetContainersRequest(uris=uris)
        res = self.stub.GetContainers(req)
        containers = [entities.Container.from_pb(pb_container) for pb_container in res.containers]
        return containers[0] if singleton else containers

    @utils.catch_rpc_error
    def _index(self, containers: List[entities.Container]):
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
    def _index_dataset(self, uri: str, record: Union[str, entities.Record, Tuple[str, Dict[str, str], datetime]],
                       instance: entities.VariableInstance, dformat: entities.DataFormat, bands: List[int],
                       min_out: float, max_out: float, exponent: float, managed: bool):
        ds_dtype = "u1"
        if isinstance(record, tuple) or dformat is None:
            try:
                with rasterio.open(uri) as ds:
                    tile = entities.Tile.from_geotransform(ds.transform, ds.crs, ds.shape[::-1])
                    ds_dtype = ds.dtypes[0]
            except Exception as e:
                raise ValueError(f'if "record" is a tuple or "bands" or "dformat" is not defined, geocube-client tries'
                                 f' to deduce some information reading the file {uri}, but it encountered'
                                 f' the following error :{e}.')

        if isinstance(record, tuple):
            aoi_id = self.create_aoi(tile.geometry(4326), exist_ok=True)

            r_name, r_tags, r_date = record
            record = self.create_record(aoi_id, name=r_name, tags=r_tags, date=r_date, exist_ok=True)

        if dformat is None:
            dformat = entities.DataFormat.from_user(ds_dtype)

        cs = [entities.Container(uri,
                                 managed=managed,
                                 datasets=[entities.Dataset(record, instance, bands=bands,
                                                            dformat=entities.DataFormat.from_user(dformat),
                                                            min_out=min_out, max_out=max_out, exponent=exponent)])]
        return self.index(cs)

    @utils.catch_rpc_error
    def _delete_datasets(self, instances: List[Union[str, entities.VariableInstance]],
                         records: List[Union[str, entities.Record]],
                         file_patterns: List[str],
                         execution_level: entities.ExecutionLevel,
                         job_name: str, allow_empty_instances: bool, allow_empty_records: bool,
                         stub=None) \
            -> entities.Job:
        if len(records) == 0 and not allow_empty_records:
            raise ValueError("DeleteDataset: records is empty, but it has not been allowed. "
                             "Empty records means that all the datasets for the given instances are about to be "
                             "deleted. If this is what is wanted, please set allow_empty_records=True")
        if len(instances) == 0 and not allow_empty_instances:
            raise ValueError("DeleteDataset: instances is empty, but it has not been allowed. "
                             "Empty instances means that all the datasets for the given records are about to be "
                             "deleted. If this is what is wanted, please set allow_empty_instances=True")

        if file_patterns is not None:
            if isinstance(file_patterns, str):
                file_patterns = [file_patterns]
            assert isinstance(file_patterns, list)

        if len(records) == 0 and len(instances) == 0:
            warnings.warn("this job may be about to delete the whole database")
            if execution_level == entities.ExecutionLevel.ASYNCHRONOUS or \
                    execution_level == entities.ExecutionLevel.SYNCHRONOUS:
                raise ValueError("I cannot allow that in a non-interactive execution_level. "
                                 "Please use execution_level == entities.ExecutionLevel.STEP_BY_STEP_CRITICAL.")
        if stub is None:
            stub = self.stub
        res = stub.DeleteDatasets(operations_pb2.DeleteDatasetsRequest(
            job_name=job_name if job_name is not None else f"Deletion_{datetime.now()}_{len(records)}_records",
            execution_level=execution_level.value,
            instance_ids=entities.get_ids(instances), record_ids=entities.get_ids(records),
            dataset_patterns=file_patterns)
        )

        return entities.Job.from_pb(self.stub, res.job)

    @utils.catch_rpc_error
    def _get_cube_metadata(self, params: entities.CubeParams) -> entities.CubeMetadata:
        cube_it = self._get_cube_it(params, headers_only=True)
        return cube_it.metadata()

    @utils.catch_rpc_error
    def _get_cube_it(self, params: entities.CubeParams, *,
                     resampling_alg: entities.Resampling = entities.Resampling.undefined,
                     headers_only: bool = False, compression: int = 0,
                     file_format = FileFormatRaw, file_pattern: str = None) -> entities.CubeIterator:
        if self.downloader is not None and not headers_only:
            metadata = self._get_cube_it(params, headers_only=True).metadata()
            if resampling_alg != entities.Resampling.undefined:
                metadata.resampling_alg = resampling_alg
            return self.downloader.get_cube_it(metadata, file_format=file_format, file_pattern=file_pattern,
                                               predownload=self.downloader.always_predownload)

        common = {
            "instances_id": [params.instance],
            "crs": params.crs,
            "pix_to_crs": layouts_pb2.GeoTransform(
                a=params.transform.c, b=params.transform.a, c=params.transform.b,
                d=params.transform.f, e=params.transform.d, f=params.transform.e),
            "size": layouts_pb2.Size(width=params.shape[0], height=params.shape[1]),
            "compression_level": compression,
            "headers_only": headers_only,
            "format": file_format,
            "resampling_alg": typing.cast(int, resampling_alg.value) - 1
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
    def _tile_aoi(self, aoi: Union[geometry.MultiPolygon, geometry.Polygon],
                  layout_name: Optional[str],
                  layout: Optional[entities.Layout],
                  resolution: Optional[float],
                  crs: Optional[str], shape: Optional[Tuple[int, int]]) -> List[entities.Tile]:
        """ TODO: use Grid or GridName """
        aoi = entities.aoi_to_pb(aoi)
        if layout_name is not None:
            req = layouts_pb2.TileAOIRequest(aoi=aoi, layout_name=layout_name)
        else:
            if layout is None:
                layout = entities.Layout.regular("", crs, shape, resolution)
            req = layouts_pb2.TileAOIRequest(aoi=aoi, layout=layout.to_pb())

        return [entities.Tile.from_pb(tile) for resp in self.stub.TileAOI(req) for tile in resp.tiles]

    @utils.catch_rpc_error
    def _get_xyz_tile(self, instance: Union[str, entities.VariableInstance],
                      records: List[Union[str, entities.Record]], x: int, y: int, z: int, file: str):
        req = catalog_pb2.GetTileRequest(
            records=records_pb2.GroupedRecordIds(ids=entities.get_ids(records)),
            instance_id=entities.get_id(instance),
            x=x, y=y, z=z)
        resp = self.stub.GetXYZTile(req)
        f = open(file, "wb")
        f.write(resp.image.data)
        f.close()

    @utils.catch_rpc_error
    def _create_layout(self, layout: entities.Layout, exist_ok):
        try:
            self.stub.CreateLayout(layouts_pb2.CreateLayoutRequest(layout=layout.to_pb()))
        except grpc.RpcError as e:
            e = utils.GeocubeError.from_rpc(e)
            if not e.is_already_exists() or not exist_ok:
                raise

    @utils.catch_rpc_error
    def _layout(self, name: str) -> entities.Layout:
        res = self.stub.ListLayouts(layouts_pb2.ListLayoutsRequest(name_like=name))
        if len(res.layouts) == 0:
            raise utils.GeocubeError("layout", grpc.StatusCode.ALREADY_EXISTS.name, "with name: " + name)
        return entities.Layout.from_pb(res.layouts[0])

    @utils.catch_rpc_error
    def _list_layouts(self, name_like: str) -> List[entities.Layout]:
        res = self.stub.ListLayouts(layouts_pb2.ListLayoutsRequest(name_like=name_like))
        return [entities.Layout.from_pb(layout) for layout in res.layouts]

    @utils.catch_rpc_error
    def _find_container_layouts(self, instance: Union[str, entities.VariableInstance],
                                records: List[Union[str, entities.Record]],
                                tags: Dict[str, str],
                                from_time: datetime, to_time: datetime,
                                aoi: geometry.MultiPolygon) -> Dict[str, List[str]]:
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
            req = catalog_pb2.FindContainerLayoutsRequest(
                instance_id=entities.get_id(instance),
                filters=records_pb2.RecordFiltersWithAOI(aoi=aoi, tags=tags,
                                                         from_time=from_time_pb, to_time=to_time_pb))
        return {resp.layout_name: resp.container_uris for resp in self.stub.FindContainerLayouts(req)}

    @utils.catch_rpc_error
    def _delete_layout(self, name: str):
        self.stub.DeleteLayout(layouts_pb2.DeleteLayoutRequest(name=name))

    @utils.catch_rpc_error
    def _create_grid(self, grid: entities.Grid):
        max_cells = min(len(grid.cells), 10000000)
        while True:
            try:
                req = [layouts_pb2.CreateGridRequest(grid=grid.to_pb(max_cells * i, max_cells * (i + 1)))
                       for i in range((len(grid.cells) - 1) // max_cells + 1)]
                return self.stub.CreateGrid(iter(req))
            except grpc.RpcError as e:
                e = utils.GeocubeError.from_rpc(e)
                if e.codename != "RESOURCE_EXHAUSTED":
                    raise
                r = parse.search("({volume:d} vs. {max:d})", e.details)
                max_cells //= max(r["volume"] // r["max"], 2)

    @utils.catch_rpc_error
    def _list_grids(self, name_like: str) -> List[entities.Grid]:
        res = self.stub.ListGrids(layouts_pb2.ListGridsRequest(name_like=name_like))
        return [entities.Grid.from_pb(grid) for grid in res.grids]

    @utils.catch_rpc_error
    def _delete_grid(self, name: str):
        self.stub.DeleteGrid(layouts_pb2.DeleteGridRequest(name=name))


    @utils.catch_rpc_error
    def _list_jobs(self, name_like: str, page: int, limit: int):
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name_like, page=page, limit=limit))
        return [entities.Job.from_pb(self.stub, r) for r in res.jobs]

    @utils.catch_rpc_error
    def _get_job_by_name(self, name: str):
        res = self.stub.ListJobs(operations_pb2.ListJobsRequest(name_like=name))
        if len(res.jobs) == 0:
            raise utils.GeocubeError("job", "NOT_FOUND", "with name: " + name)
        return entities.Job.from_pb(self.stub, res.jobs[0])

    @utils.catch_rpc_error
    def _get_job_by_id(self, job_id: Union[str, entities.Job], log_page, log_limit):
        res = self.stub.GetJob(operations_pb2.GetJobRequest(id=entities.get_id(job_id),
                                                            log_page=log_page, log_limit=log_limit))
        return entities.Job.from_pb(self.stub, res.job)

    @utils.catch_rpc_error
    def _remove_terminated_jobs(self, name_like: str, state: str):
        self.stub.CleanJobs(operations_pb2.CleanJobsRequest(name_like=name_like, state=state))

    @utils.catch_rpc_error
    def _consolidate(self,
                     job_name: str,
                     instance: Union[str, entities.VariableInstance],
                     layout: Union[str, entities.Layout],
                     records: Union[List[entities.RecordIdentifiers], None],
                     tags: Union[Dict[str, str], None],
                     from_time: Union[datetime, None],
                     to_time: Union[datetime, None],
                     collapse_on_record: Union[entities.Record, str, None],
                     execution_level: entities.ExecutionLevel):
        common = {
            "job_name":              job_name,
            "instance_id":           entities.get_id(instance),
            "layout_name":           entities.get_id(layout),
            "execution_level":       execution_level.value,
            "collapse_on_record_id": entities.get_id(collapse_on_record) if collapse_on_record is not None else "",
        }

        if records is not None:
            req = operations_pb2.ConsolidateRequest(
                **common, records=records_pb2.RecordIdList(ids=entities.get_ids(records)))
            if from_time is not None:
                warnings.warn("from_time is ignored if records is provided as argument to consolidate")
            if to_time is not None:
                warnings.warn("to_time is ignored if records is provided as argument to consolidate")
            if tags is not None:
                warnings.warn("tags is ignored if records is provided as argument to consolidate")
        else:
            from_time_pb = utils.pb_null_timestamp()
            if from_time is not None:
                from_time_pb.FromDatetime(from_time)
            to_time_pb = utils.pb_null_timestamp()
            if to_time is not None:
                to_time_pb.FromDatetime(to_time)
            req = operations_pb2.ConsolidateRequest(**common, filters=records_pb2.RecordFilters(
                tags=tags, from_time=from_time_pb, to_time=to_time_pb
            ))
        return self.get_job(self.stub.Consolidate(req).job_id)

class Consolidater(Client):
    """ Deprecated: use Client instead """
