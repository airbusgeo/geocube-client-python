import errno
import os
import zlib
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from geocube.pb import catalog_pb2

from geocube import entities, utils


class CubeIterator:
    """
    Iterator on a cube of datasets from the Geocube Server

    Yields
    -------
    - array, Image or filename depending on options
    - list of record composing the image
    - error or None
    - download_size
    """
    @dataclass
    class Image:
        dtype: np.dtype
        shape: Tuple[float, float, float]
        data:  bytearray
        pass

    def __init__(self, get_cube_stream, file_format, file_pattern: str):
        self.stream = iter(get_cube_stream)
        self.file_format = file_format
        self.file_pattern = file_pattern

        # Get Global header
        resp = next(self.stream)
        if resp.global_header is None:
            raise ValueError("Expecting global header")
        self.count = resp.global_header.count
        self.nb_datasets = resp.global_header.nb_datasets

    def __len__(self):
        return self.count

    def __iter__(self):
        self.num = 0
        return self

    @utils.catch_rpc_error
    def __next__(self):
        # Get Header
        header = next(self.stream).header

        if header is None:
            raise ValueError("Expecting header")
        if header.error != "":
            self.count -= 1
            return None, None, header.error, 0

        self.num += 1
        nb_parts = header.nb_parts
        image = CubeIterator.Image(
            np.dtype(entities.dataformat.pb_types[header.dtype]),
            (header.shape.dim3, header.shape.dim2, header.shape.dim1),
            bytearray(header.data))

        image.dtype.newbyteorder('>' if header.order == catalog_pb2.BigEndian else '<')
        records = []
        for r in header.records:
            records.append(entities.Record.from_pb(r))

        if nb_parts == 0:
            return image, records, None, image.shape[0]*image.shape[1]*image.shape[2]*image.dtype.itemsize

        # Get chunks
        for part in range(1, nb_parts):
            resp = next(self.stream)
            if resp.chunk is None or resp.chunk.part != part:
                raise ValueError("Expecting chunk")
            image.data += bytearray(resp.chunk.data)

        # Inflate data
        # (-15: window size logarithm. The input must be a raw stream with no header or trailer)
        buf = zlib.decompress(image.data, -15, np.prod(image.shape)*image.dtype.itemsize)

        if self.file_format == catalog_pb2.Raw:
            return np.frombuffer(buf, dtype=image.dtype).reshape(image.shape), records, None, len(image.data)

        if self.file_format == catalog_pb2.GTiff:
            filename = self.file_pattern.replace('{#}', str(self.num))
            min_date = min(r.datetime for r in records).strftime("%Y-%m-%d_%H:%M:%S")
            max_date = max(r.datetime for r in records).strftime("%Y-%m-%d_%H:%M:%S")
            filename = filename.replace('{date}', min_date if min_date == max_date else min_date+"_"+max_date)
            filename = filename.replace('{id}', '_'.join([r.id for r in records]))
            filename = filename.replace('{name}', records[0].name)
            dir_name = os.path.dirname(filename)
            if dir_name != '' and not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            f = open(filename, "wb")
            f.write(buf)
            f.close()
            return filename, records, None, len(image.data)
