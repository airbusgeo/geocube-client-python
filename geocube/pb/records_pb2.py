# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/records.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18geocube/pb/records.proto\x12\x07geocube\x1a\x1fgoogle/protobuf/timestamp.proto\"!\n\x05\x43oord\x12\x0b\n\x03lon\x18\x01 \x01(\x02\x12\x0b\n\x03lat\x18\x02 \x01(\x02\",\n\nLinearRing\x12\x1e\n\x06points\x18\x01 \x03(\x0b\x32\x0e.geocube.Coord\"3\n\x07Polygon\x12(\n\x0blinearrings\x18\x01 \x03(\x0b\x32\x13.geocube.LinearRing\")\n\x03\x41OI\x12\"\n\x08polygons\x18\x01 \x03(\x0b\x32\x10.geocube.Polygon\"\xcd\x01\n\x06Record\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x04time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x04tags\x18\x04 \x03(\x0b\x32\x19.geocube.Record.TagsEntry\x12\x0e\n\x06\x61oi_id\x18\x05 \x01(\t\x12\x19\n\x03\x61oi\x18\x06 \x01(\x0b\x32\x0c.geocube.AOI\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xac\x01\n\tNewRecord\x12\x0c\n\x04name\x18\x01 \x01(\t\x12(\n\x04time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x04tags\x18\x03 \x03(\x0b\x32\x1c.geocube.NewRecord.TagsEntry\x12\x0e\n\x06\x61oi_id\x18\x04 \x01(\t\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x1b\n\x0cRecordIdList\x12\x0b\n\x03ids\x18\x01 \x03(\t\"2\n\x0eGroupedRecords\x12 \n\x07records\x18\x01 \x03(\x0b\x32\x0f.geocube.Record\"\x1f\n\x10GroupedRecordIds\x12\x0b\n\x03ids\x18\x01 \x03(\t\"B\n\x14GroupedRecordIdsList\x12*\n\x07records\x18\x01 \x03(\x0b\x32\x19.geocube.GroupedRecordIds\";\n\x14\x43reateRecordsRequest\x12#\n\x07records\x18\x01 \x03(\x0b\x32\x12.geocube.NewRecord\"$\n\x15\x43reateRecordsResponse\x12\x0b\n\x03ids\x18\x01 \x03(\t\" \n\x11GetRecordsRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"9\n\x16GetRecordsResponseItem\x12\x1f\n\x06record\x18\x01 \x01(\x0b\x32\x0f.geocube.Record\"4\n\x14\x44\x65leteRecordsRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\x0f\n\x07no_fail\x18\x02 \x01(\x08\"#\n\x15\x44\x65leteRecordsResponse\x12\n\n\x02nb\x18\x01 \x01(\x03\"\x89\x01\n\x15\x41\x64\x64RecordsTagsRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\x36\n\x04tags\x18\x02 \x03(\x0b\x32(.geocube.AddRecordsTagsRequest.TagsEntry\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"$\n\x16\x41\x64\x64RecordsTagsResponse\x12\n\n\x02nb\x18\x01 \x01(\x03\"8\n\x18RemoveRecordsTagsRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\x0f\n\x07tagsKey\x18\x02 \x03(\t\"\'\n\x19RemoveRecordsTagsResponse\x12\n\n\x02nb\x18\x01 \x01(\x03\"-\n\x10\x43reateAOIRequest\x12\x19\n\x03\x61oi\x18\x01 \x01(\x0b\x32\x0c.geocube.AOI\"\x1f\n\x11\x43reateAOIResponse\x12\n\n\x02id\x18\x01 \x01(\t\"\x1b\n\rGetAOIRequest\x12\n\n\x02id\x18\x01 \x01(\t\"+\n\x0eGetAOIResponse\x12\x19\n\x03\x61oi\x18\x01 \x01(\x0b\x32\x0c.geocube.AOI\"\xaa\x02\n\x12ListRecordsRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x33\n\x04tags\x18\x03 \x03(\x0b\x32%.geocube.ListRecordsRequest.TagsEntry\x12-\n\tfrom_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\x07to_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x19\n\x03\x61oi\x18\x08 \x01(\x0b\x32\x0c.geocube.AOI\x12\r\n\x05limit\x18\x06 \x01(\x05\x12\x0c\n\x04page\x18\x07 \x01(\x05\x12\x10\n\x08with_aoi\x18\t \x01(\x08\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\":\n\x17ListRecordsResponseItem\x12\x1f\n\x06record\x18\x01 \x01(\x0b\x32\x0f.geocube.Record\"\xc8\x01\n\rRecordFilters\x12.\n\x04tags\x18\x01 \x03(\x0b\x32 .geocube.RecordFilters.TagsEntry\x12-\n\tfrom_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\x07to_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"Z\n\x14RecordFiltersWithAOI\x12\'\n\x07\x66ilters\x18\x01 \x01(\x0b\x32\x16.geocube.RecordFilters\x12\x19\n\x03\x61oi\x18\x02 \x01(\x0b\x32\x0c.geocube.AOIB\x0eZ\x0c./pb;geocubeb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'geocube.pb.records_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\014./pb;geocube'
  _globals['_RECORD_TAGSENTRY']._options = None
  _globals['_RECORD_TAGSENTRY']._serialized_options = b'8\001'
  _globals['_NEWRECORD_TAGSENTRY']._options = None
  _globals['_NEWRECORD_TAGSENTRY']._serialized_options = b'8\001'
  _globals['_ADDRECORDSTAGSREQUEST_TAGSENTRY']._options = None
  _globals['_ADDRECORDSTAGSREQUEST_TAGSENTRY']._serialized_options = b'8\001'
  _globals['_LISTRECORDSREQUEST_TAGSENTRY']._options = None
  _globals['_LISTRECORDSREQUEST_TAGSENTRY']._serialized_options = b'8\001'
  _globals['_RECORDFILTERS_TAGSENTRY']._options = None
  _globals['_RECORDFILTERS_TAGSENTRY']._serialized_options = b'8\001'
  _globals['_COORD']._serialized_start=70
  _globals['_COORD']._serialized_end=103
  _globals['_LINEARRING']._serialized_start=105
  _globals['_LINEARRING']._serialized_end=149
  _globals['_POLYGON']._serialized_start=151
  _globals['_POLYGON']._serialized_end=202
  _globals['_AOI']._serialized_start=204
  _globals['_AOI']._serialized_end=245
  _globals['_RECORD']._serialized_start=248
  _globals['_RECORD']._serialized_end=453
  _globals['_RECORD_TAGSENTRY']._serialized_start=410
  _globals['_RECORD_TAGSENTRY']._serialized_end=453
  _globals['_NEWRECORD']._serialized_start=456
  _globals['_NEWRECORD']._serialized_end=628
  _globals['_NEWRECORD_TAGSENTRY']._serialized_start=410
  _globals['_NEWRECORD_TAGSENTRY']._serialized_end=453
  _globals['_RECORDIDLIST']._serialized_start=630
  _globals['_RECORDIDLIST']._serialized_end=657
  _globals['_GROUPEDRECORDS']._serialized_start=659
  _globals['_GROUPEDRECORDS']._serialized_end=709
  _globals['_GROUPEDRECORDIDS']._serialized_start=711
  _globals['_GROUPEDRECORDIDS']._serialized_end=742
  _globals['_GROUPEDRECORDIDSLIST']._serialized_start=744
  _globals['_GROUPEDRECORDIDSLIST']._serialized_end=810
  _globals['_CREATERECORDSREQUEST']._serialized_start=812
  _globals['_CREATERECORDSREQUEST']._serialized_end=871
  _globals['_CREATERECORDSRESPONSE']._serialized_start=873
  _globals['_CREATERECORDSRESPONSE']._serialized_end=909
  _globals['_GETRECORDSREQUEST']._serialized_start=911
  _globals['_GETRECORDSREQUEST']._serialized_end=943
  _globals['_GETRECORDSRESPONSEITEM']._serialized_start=945
  _globals['_GETRECORDSRESPONSEITEM']._serialized_end=1002
  _globals['_DELETERECORDSREQUEST']._serialized_start=1004
  _globals['_DELETERECORDSREQUEST']._serialized_end=1056
  _globals['_DELETERECORDSRESPONSE']._serialized_start=1058
  _globals['_DELETERECORDSRESPONSE']._serialized_end=1093
  _globals['_ADDRECORDSTAGSREQUEST']._serialized_start=1096
  _globals['_ADDRECORDSTAGSREQUEST']._serialized_end=1233
  _globals['_ADDRECORDSTAGSREQUEST_TAGSENTRY']._serialized_start=410
  _globals['_ADDRECORDSTAGSREQUEST_TAGSENTRY']._serialized_end=453
  _globals['_ADDRECORDSTAGSRESPONSE']._serialized_start=1235
  _globals['_ADDRECORDSTAGSRESPONSE']._serialized_end=1271
  _globals['_REMOVERECORDSTAGSREQUEST']._serialized_start=1273
  _globals['_REMOVERECORDSTAGSREQUEST']._serialized_end=1329
  _globals['_REMOVERECORDSTAGSRESPONSE']._serialized_start=1331
  _globals['_REMOVERECORDSTAGSRESPONSE']._serialized_end=1370
  _globals['_CREATEAOIREQUEST']._serialized_start=1372
  _globals['_CREATEAOIREQUEST']._serialized_end=1417
  _globals['_CREATEAOIRESPONSE']._serialized_start=1419
  _globals['_CREATEAOIRESPONSE']._serialized_end=1450
  _globals['_GETAOIREQUEST']._serialized_start=1452
  _globals['_GETAOIREQUEST']._serialized_end=1479
  _globals['_GETAOIRESPONSE']._serialized_start=1481
  _globals['_GETAOIRESPONSE']._serialized_end=1524
  _globals['_LISTRECORDSREQUEST']._serialized_start=1527
  _globals['_LISTRECORDSREQUEST']._serialized_end=1825
  _globals['_LISTRECORDSREQUEST_TAGSENTRY']._serialized_start=410
  _globals['_LISTRECORDSREQUEST_TAGSENTRY']._serialized_end=453
  _globals['_LISTRECORDSRESPONSEITEM']._serialized_start=1827
  _globals['_LISTRECORDSRESPONSEITEM']._serialized_end=1885
  _globals['_RECORDFILTERS']._serialized_start=1888
  _globals['_RECORDFILTERS']._serialized_end=2088
  _globals['_RECORDFILTERS_TAGSENTRY']._serialized_start=410
  _globals['_RECORDFILTERS_TAGSENTRY']._serialized_end=453
  _globals['_RECORDFILTERSWITHAOI']._serialized_start=2090
  _globals['_RECORDFILTERSWITHAOI']._serialized_end=2180
# @@protoc_insertion_point(module_scope)
