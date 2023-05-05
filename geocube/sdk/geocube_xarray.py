import copy
from typing import Tuple, List, Any

import numpy as np
import xarray
from geocube.entities import cubeiterator
from xarray.backends import BackendEntrypoint, BackendArray
from xarray.core import indexing as xarray_indexing

from geocube import entities, sdk
from geocube.utils import SparseFullArray, indexing


def open_geocube(
        collection: sdk.Collection,
        connection_params: sdk.ConnectionParams,
        downloader_params: sdk.ConnectionParams = None,
        block_size: Tuple[int, int] = None,
        chunks=None,
        **kwargs,
):
    """Load and decode a dataset from a Geocube.

    The `cube_params` object should be a valid Collection

    Args:
        chunks
        collection :
        connection_params : connection parameters to a geocube
        downloader_params : connection parameters to a downloader
        block_size: internal block_size of the layout

    Returns:
        The newly created dataset.

    References:
        http://github.com/airbusgeo/geocube
    """

    from xarray import open_dataset

    if kwargs:
        raise TypeError(
            "open_geocube() got unexpected keyword arguments " + ",".join(kwargs.keys())
        )

    if not isinstance(collection, sdk.Collection):
        raise TypeError(
            f"open_geocube() got unexpected collection argument: {collection}"
        )

    if block_size is not None:
        chunks = {}

    backend_kwargs = {
        "connection_params": connection_params,
        "downloader_params": downloader_params,
        "block_size":        block_size,
    }

    ds = open_dataset(
        filename_or_obj=collection,
        engine=GeocubeBackendEntrypoint,
        backend_kwargs=backend_kwargs,
        chunks=chunks,
        drop_variables=None,
    )
    return ds


class GeocubeBackendEntrypoint(BackendEntrypoint):
    def open_dataset(
            self,
            collection: sdk.Collection,
            # mask_and_scale: bool = True, FillValue with NA and original_values * scale_factor + add_offset
            # decode_times: bool = True, Otherwise, leave datetime encoded as numbers
            connection_params: sdk.ConnectionParams = sdk.ConnectionParams("127.0.0.1:8080"),
            downloader_params: sdk.ConnectionParams = None,
            block_size: Tuple[int, int] = None,
            drop_variables=None  # ignored
    ):
        if downloader_params is not None:
            connection_params.use_downloader(downloader_params)
        if drop_variables is not None:
            raise ValueError("geocube_xarray does not support drop_variables")
        # Read variables
        client = connection_params.new_client()
        variables = collection.variables(client)

        # Load axis information
        cube_params = collection.cube_params(client, "")
        bbox = cube_params.transform*(0, 0) + cube_params.transform*cube_params.shape
        record_keys = collection.record_keys(client)
        record_ids = collection.record_ids(client)
        shape = (cube_params.shape[1], cube_params.shape[0], len(record_keys))
        coordinates = {
            "y": np.linspace(bbox[1], bbox[3], shape[0]),
            "x": np.linspace(bbox[0], bbox[2], shape[1]),
            "key": record_keys
        }

        data_vars = {}
        for variable in variables:
            var_unique_name = f"{variable.variable_name}:{variable.instance_name}"
            # Get shape
            if len(variable.bands) > 1:
                var_shape = shape[0:2] + (len(variable.bands),) + shape[-1:]
                bands = var_unique_name + ":bands"
                coordinates[bands] = variable.bands
                dims = ["y", "x", bands, "key"]
            else:
                var_shape = shape
                dims = ["y", "x", "key"]

            # Create backend
            cp = collection.cube_params(client, variable.instance_id)
            cp.records = record_ids
            backend_array = GeocubeBackendArray(cp,
                                                connection_params,
                                                record_keys, variable.dformat.dtype, var_shape,
                                                collection.group_key_func)
            data = xarray_indexing.LazilyIndexedArray(backend_array)
            encoding = {}
            if block_size is not None:
                encoding["preferred_chunks"] = {"x": block_size[0], "y": block_size[1]}
            data_vars[var_unique_name] =\
                xarray.Variable(dims, data, attrs=variable.metadata, encoding=encoding)

        return xarray.Dataset(data_vars, coords=coordinates)

    def guess_can_open(self, filename_or_obj):
        return isinstance(filename_or_obj, sdk.Collection)


class GeocubeBackendArray(BackendArray):
    def __init__(self, cube_params: entities.CubeParams, connection_params: sdk.ConnectionParams,
                 record_keys: List[Any], dtype, shape, group_key_func: entities.GroupByKeyFunc = None):
        self.cube_params = copy.deepcopy(cube_params)
        self.connection_params = connection_params
        self.record_keys = record_keys
        self.shape = shape
        self.dtype = dtype
        self._has_bands = len(shape) > 3
        self.record_key_func = group_key_func if group_key_func is not None else entities.Record.key_datetime

    def __getitem__(
        self, key: xarray_indexing.ExplicitIndexer
    ) -> np.ndarray:
        return xarray_indexing.explicit_indexing_adapter(
            key,
            self.shape,
            xarray_indexing.IndexingSupport.BASIC,
            self._raw_indexing_method,
        )

    def _raw_indexing_method(self, key: tuple) -> np.ndarray:
        client = self.connection_params.new_client(with_downloader=True)

        # Pixel coordinates
        i_1, i_2, _, key_i = indexing.key_to_range(key[0], self.shape[0])
        j_1, j_2, _, key_j = indexing.key_to_range(key[1], self.shape[1])

        # (i, j) are (y, x) coordinates. They must be swapped in reshape().
        tile = self.cube_params.tile.reshape(j_1, i_1, j_2, i_2)

        assert len(self.cube_params.records) == len(self.record_keys)
        grouped_records = self.cube_params.records[key[-1]]
        cp = entities.CubeParams.from_tile(tile,
                                           instance=self.cube_params.instance,
                                           records=grouped_records)

        cube_it = client.get_cube_it(cp)
        shape = (cp.shape[1], cp.shape[0], *self.shape[2:-1], len(grouped_records))  # w,h[,b],t
        timeseries = SparseFullArray(shape, -1)

        for image, metadata, err in cube_it:
            if err is not None:
                if err == cubeiterator.NOT_FOUND_ERROR:
                    continue
                raise ValueError(err)
            i = self.record_keys.index(self.record_key_func(metadata.grouped_records[0]))
            timeseries.put(i, image.reshape(timeseries.shape[:-1]))

        if self._has_bands:
            return timeseries[key_i, key_j, key[2], :]
        return timeseries[key_i, key_j, :]


# BACKEND_ENTRYPOINTS["geocube"] = GeocubeBackendEntrypoint
