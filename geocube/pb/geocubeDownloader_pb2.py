# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/geocubeDownloader.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from geocube.pb import version_pb2 as geocube_dot_pb_dot_version__pb2
from geocube.pb import catalog_pb2 as geocube_dot_pb_dot_catalog__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"geocube/pb/geocubeDownloader.proto\x12\x07geocube\x1a\x18geocube/pb/version.proto\x1a\x18geocube/pb/catalog.proto2\xb0\x01\n\x11GeocubeDownloader\x12U\n\x0c\x44ownloadCube\x12\x1f.geocube.GetCubeMetadataRequest\x1a .geocube.GetCubeMetadataResponse\"\x00\x30\x01\x12\x44\n\x07Version\x12\x1a.geocube.GetVersionRequest\x1a\x1b.geocube.GetVersionResponse\"\x00\x42\x0eZ\x0c./pb;geocubeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'geocube.pb.geocubeDownloader_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\014./pb;geocube'
  _globals['_GEOCUBEDOWNLOADER']._serialized_start=100
  _globals['_GEOCUBEDOWNLOADER']._serialized_end=276
# @@protoc_insertion_point(module_scope)
