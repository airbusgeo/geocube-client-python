# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/admin.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from geocube.pb import dataformat_pb2 as geocube_dot_pb_dot_dataformat__pb2
from geocube.pb import operations_pb2 as geocube_dot_pb_dot_operations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16geocube/pb/admin.proto\x12\x07geocube\x1a\x1bgeocube/pb/dataformat.proto\x1a\x1bgeocube/pb/operations.proto\"\xb4\x01\n\rTidyDBRequest\x12\x10\n\x08Simulate\x18\x01 \x01(\x08\x12\x13\n\x0bPendingAOIs\x18\x02 \x01(\x08\x12\x16\n\x0ePendingRecords\x18\x03 \x01(\x08\x12\x18\n\x10PendingVariables\x18\x04 \x01(\x08\x12\x18\n\x10PendingInstances\x18\x05 \x01(\x08\x12\x19\n\x11PendingContainers\x18\x06 \x01(\x08\x12\x15\n\rPendingParams\x18\x07 \x01(\x08\"\x85\x01\n\x0eTidyDBResponse\x12\x0e\n\x06NbAOIs\x18\x01 \x01(\x03\x12\x11\n\tNbRecords\x18\x02 \x01(\x03\x12\x13\n\x0bNbVariables\x18\x03 \x01(\x03\x12\x13\n\x0bNbInstances\x18\x04 \x01(\x03\x12\x14\n\x0cNbContainers\x18\x05 \x01(\x03\x12\x10\n\x08NbParams\x18\x06 \x01(\x03\"\xba\x01\n\x15UpdateDatasetsRequest\x12\x10\n\x08simulate\x18\x01 \x01(\x08\x12\x13\n\x0binstance_id\x18\x02 \x01(\t\x12\x12\n\nrecord_ids\x18\x03 \x03(\t\x12$\n\x07\x64\x66ormat\x18\x08 \x01(\x0b\x32\x13.geocube.DataFormat\x12\x16\n\x0ereal_min_value\x18\t \x01(\x01\x12\x16\n\x0ereal_max_value\x18\n \x01(\x01\x12\x10\n\x08\x65xponent\x18\x0b \x01(\x01\"\x87\x01\n\x16UpdateDatasetsResponse\x12=\n\x07results\x18\x01 \x03(\x0b\x32,.geocube.UpdateDatasetsResponse.ResultsEntry\x1a.\n\x0cResultsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\"\x9f\x01\n\x15\x44\x65leteDatasetsRequest\x12\x12\n\nrecord_ids\x18\x02 \x03(\t\x12\x14\n\x0cinstance_ids\x18\x03 \x03(\t\x12\x18\n\x10\x64\x61taset_patterns\x18\x06 \x03(\t\x12\x30\n\x0f\x65xecution_level\x18\x04 \x01(\x0e\x32\x17.geocube.ExecutionLevel\x12\x10\n\x08job_name\x18\x05 \x01(\t\"3\n\x16\x44\x65leteDatasetsResponse\x12\x19\n\x03job\x18\x02 \x01(\x0b\x32\x0c.geocube.Job2\xee\x01\n\x05\x41\x64min\x12;\n\x06TidyDB\x12\x16.geocube.TidyDBRequest\x1a\x17.geocube.TidyDBResponse\"\x00\x12S\n\x0eUpdateDatasets\x12\x1e.geocube.UpdateDatasetsRequest\x1a\x1f.geocube.UpdateDatasetsResponse\"\x00\x12S\n\x0e\x44\x65leteDatasets\x12\x1e.geocube.DeleteDatasetsRequest\x1a\x1f.geocube.DeleteDatasetsResponse\"\x00\x42\x0eZ\x0c./pb;geocubeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'geocube.pb.admin_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\014./pb;geocube'
  _globals['_UPDATEDATASETSRESPONSE_RESULTSENTRY']._options = None
  _globals['_UPDATEDATASETSRESPONSE_RESULTSENTRY']._serialized_options = b'8\001'
  _globals['_TIDYDBREQUEST']._serialized_start=94
  _globals['_TIDYDBREQUEST']._serialized_end=274
  _globals['_TIDYDBRESPONSE']._serialized_start=277
  _globals['_TIDYDBRESPONSE']._serialized_end=410
  _globals['_UPDATEDATASETSREQUEST']._serialized_start=413
  _globals['_UPDATEDATASETSREQUEST']._serialized_end=599
  _globals['_UPDATEDATASETSRESPONSE']._serialized_start=602
  _globals['_UPDATEDATASETSRESPONSE']._serialized_end=737
  _globals['_UPDATEDATASETSRESPONSE_RESULTSENTRY']._serialized_start=691
  _globals['_UPDATEDATASETSRESPONSE_RESULTSENTRY']._serialized_end=737
  _globals['_DELETEDATASETSREQUEST']._serialized_start=740
  _globals['_DELETEDATASETSREQUEST']._serialized_end=899
  _globals['_DELETEDATASETSRESPONSE']._serialized_start=901
  _globals['_DELETEDATASETSRESPONSE']._serialized_end=952
  _globals['_ADMIN']._serialized_start=955
  _globals['_ADMIN']._serialized_end=1193
# @@protoc_insertion_point(module_scope)
