from __future__ import annotations

import typing
from typing import List, Tuple

import grpc
import numpy as np

from geocube.pb import records_pb2, catalog_pb2, layouts_pb2, geocubeDownloader_pb2_grpc as downloader_grpc, \
    datasetMeta_pb2, version_pb2
from geocube import entities, utils

FileFormatRaw = catalog_pb2.Raw
FileFormatGTiff = catalog_pb2.GTiff


class Downloader:
    def __init__(self, uri: str, secure: bool = False, api_key: str = "", verbose: bool = True):
        """
        Initialise the connexion to the Geocube Downloader

        Args:
            uri: of the Geocube Downloader
            secure: True to use a TLS Connexion
            api_key: (optional) API Key if Geocube Server is secured using a bearer authentication
            verbose: display the version of the Geocube Server
        """
        if secure:
            credentials = grpc.ssl_channel_credentials()
            if api_key != "":
                token_credentials = grpc.access_token_call_credentials(api_key)
                credentials = grpc.composite_channel_credentials(credentials, token_credentials)
            self._channel = grpc.secure_channel(uri, credentials)
        else:
            self._channel = grpc.insecure_channel(uri)
        self.stub = downloader_grpc.GeocubeDownloaderStub(self._channel)
        if verbose:
            print("Connected to Geocube Downloader v" + self.version())

    @utils.catch_rpc_error
    def version(self) -> str:
        """ Returns the version of the Geocube Server """
        return self.stub.Version(version_pb2.GetVersionRequest()).Version

    @utils.catch_rpc_error
    def get_cube(self, metadata: entities.CubeMetadata, verbose: bool = True) \
            -> Tuple[List[np.array], List[entities.GroupedRecords]]:
        """
        Get a cube given a CubeParameters

        Args:
            metadata: CubeMetadata (see entities.CubeMetadata and entities.CubeIterator)
            verbose: add information during the transfer

        Returns:
            list of images (np.ndarray) and the list of corresponding records
                (several records can be returned for each image when they are grouped together,
                by date or something else. See entities.Record.group_by)
        """
        cube = self._get_cube_it(metadata)
        images, grouped_records = [], []
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
                print("Image {} received ({}kb) RecordTime:{} RecordName:{} Shape:{}".format(
                    cube.index+1, metadata.bytes//1024,
                    min_date if min_date == max_date else min_date + " to " + max_date,
                    metadata.grouped_records[0].name, image.shape))
            images.append(image)
            grouped_records.append(metadata.grouped_records)
        return images, grouped_records

    @utils.catch_rpc_error
    def get_cube_it(self, metadata: entities.CubeMetadata, file_format=FileFormatRaw, file_pattern: str = None)\
            -> entities.CubeIterator:
        """
        Returns a cube iterator over the requested images

        Args:
            metadata: CubeMetadata (see entities.CubeMetadata and entities.CubeIterator)
            file_format: (optional) currently supported geocube.FileFormatRaw & geocube.FileFormatGTiff
            file_pattern: (optional) iif file_format != Raw, pattern of the file name.
                {#} will be replaced by the number of image, {date} and {id} by the value of the record

        Returns:
            an iterator yielding an image, its associated records, an error (or None) and the size of the image
        """
        return self._get_cube_it(metadata, file_format, file_pattern)

    def _get_cube_it(self, metadata: entities.CubeMetadata, file_format=FileFormatRaw, file_pattern: str = None)\
            -> entities.CubeIterator:
        req = catalog_pb2.GetCubeMetadataRequest(
            grouped_records=[records_pb2.GroupedRecords(records=[r.to_pb() for r in s.grouped_records])
                             for s in metadata.slices],
            datasets_meta=[datasetMeta_pb2.DatasetMeta(internalsMeta=s.metadata) for s in metadata.slices],
            ref_dformat=metadata.dformat.to_pb(),
            resampling_alg=typing.cast(int, metadata.resampling_alg.value)-1,
            crs=metadata.crs,
            pix_to_crs=layouts_pb2.GeoTransform(
                a=metadata.transform.c, b=metadata.transform.a, c=metadata.transform.b,
                d=metadata.transform.f, e=metadata.transform.d, f=metadata.transform.e),
            size=layouts_pb2.Size(width=metadata.shape[0], height=metadata.shape[1]),
            format=file_format
        )

        return entities.CubeIterator(self.stub.DownloadCube(req), file_format, file_pattern)
