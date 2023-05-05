import errno
import os
import zlib
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from geocube.pb import catalog_pb2

from geocube import entities, utils

NOT_FOUND_ERROR = "rpc error: code = NotFound desc = Not enough valid pixels (skipped)"


class CubeIterator:
    """
    Iterator on a cube of datasets from the Geocube Server

    Yields:
        - ndarray, ArrayLike or filename depending on options.
        @warning CubeIterator might not own the returned ndarray.
        To update the returned image, check ndarray.flags.writeable and use ndarray.copy() if necessary.
        - metadata, including a list of records composing the image
        - error or None
    """
    @dataclass
    class ArrayLike:
        dtype: np.dtype
        shape: Tuple[float, float, float]

    def __init__(self, get_cube_stream, file_format, file_pattern: str):
        self.stream = iter(get_cube_stream)
        self.file_format = file_format
        self.file_pattern = file_pattern
        self.index = -1

        # Get Global header
        resp = next(self.stream)
        if resp.global_header is None:
            raise ValueError("Expecting global header")
        self.count = resp.global_header.count
        self.nb_datasets = resp.global_header.nb_datasets
        self._cube_metadata = entities.CubeMetadata.from_pb(resp.global_header)

    def __len__(self):
        return self.count

    def __iter__(self):
        self.index = -1
        return self

    @utils.catch_rpc_error
    def __next__(self):
        # Get Header
        header = next(self.stream).header
        if header is None:
            raise ValueError("Expecting header")
        if header.error != "":
            self.count -= 1
            return None, None, header.error

        self.index += 1
        image = CubeIterator.ArrayLike(
            dtype=np.dtype(entities.dataformat.pb_types[header.dtype]),
            shape=(header.shape.dim3, header.shape.dim2, header.shape.dim1),
            )
        image.dtype.newbyteorder('>' if header.order == catalog_pb2.BigEndian else '<')

        metadata = entities.SliceMetadata(
            grouped_records=[entities.Record.from_pb(r) for r in header.grouped_records.records],
            metadata=header.dataset_meta.internalsMeta,
            bytes=np.prod(image.shape)*image.dtype.itemsize
        )
        self._cube_metadata.shape = (header.shape.dim2, header.shape.dim3)
        self._cube_metadata.slices.append(metadata)

        if header.nb_parts == 0:
            return image, metadata, None

        # Get chunks
        data = bytearray(header.data)
        for part in range(1, header.nb_parts):
            resp = next(self.stream)
            if resp.chunk is None or resp.chunk.part != part:
                raise ValueError("Expecting chunk")
            data += bytearray(resp.chunk.data)
        metadata.bytes = len(data)

        # Inflate data
        # (-15: window size logarithm. The input must be a raw stream with no header or trailer)
        if header.compression:
            data = zlib.decompress(data, -15, np.prod(image.shape)*image.dtype.itemsize)

        if self.file_format == catalog_pb2.Raw:
            return np.ndarray(image.shape, image.dtype, data), metadata, None

        if self.file_format == catalog_pb2.GTiff:
            filename = self.file_pattern.replace('{#}', str(self.index+1))
            min_date = metadata.min_date.strftime("%Y-%m-%d_%H:%M:%S")
            max_date = metadata.max_date.strftime("%Y-%m-%d_%H:%M:%S")
            filename = filename.replace('{date}', min_date if min_date == max_date else min_date+"_"+max_date)
            filename = filename.replace('{id}', '_'.join(entities.get_ids(metadata.grouped_records)))
            filename = filename.replace('{name}', metadata.grouped_records[0].name)
            dir_name = os.path.dirname(filename)
            if dir_name != '' and not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            f = open(filename, "wb")
            f.write(data)
            f.close()
            return filename, metadata, None

    def metadata(self) -> entities.CubeMetadata:
        for _, _, _ in self:
            pass
        return self._cube_metadata
