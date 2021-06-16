# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/catalog.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from geocube.pb import dataformat_pb2 as geocube_dot_pb_dot_dataformat__pb2
from geocube.pb import records_pb2 as geocube_dot_pb_dot_records__pb2
from geocube.pb import layouts_pb2 as geocube_dot_pb_dot_layouts__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='geocube/pb/catalog.proto',
  package='geocube',
  syntax='proto3',
  serialized_options=b'Z\014./pb;geocube',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18geocube/pb/catalog.proto\x12\x07geocube\x1a\x1bgeocube/pb/dataformat.proto\x1a\x18geocube/pb/records.proto\x1a\x18geocube/pb/layouts.proto\"1\n\x05Shape\x12\x0c\n\x04\x64im1\x18\x01 \x01(\x05\x12\x0c\n\x04\x64im2\x18\x02 \x01(\x05\x12\x0c\n\x04\x64im3\x18\x03 \x01(\x05\"\xed\x01\n\x0bImageHeader\x12\x1d\n\x05shape\x18\x01 \x01(\x0b\x32\x0e.geocube.Shape\x12(\n\x05\x64type\x18\x02 \x01(\x0e\x32\x19.geocube.DataFormat.Dtype\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x10\n\x08nb_parts\x18\x04 \x01(\x05\x12\x0c\n\x04size\x18\x05 \x01(\x03\x12!\n\x05order\x18\x06 \x01(\x0e\x32\x12.geocube.ByteOrder\x12\x13\n\x0b\x63ompression\x18\x07 \x01(\x08\x12 \n\x07records\x18\x08 \x03(\x0b\x32\x0f.geocube.Record\x12\r\n\x05\x65rror\x18\t \x01(\t\"(\n\nImageChunk\x12\x0c\n\x04part\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x19\n\tImageFile\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\xe7\x02\n\x0eGetCubeRequest\x12&\n\x07records\x18\x01 \x01(\x0b\x32\x13.geocube.RecordListH\x00\x12)\n\x07\x66ilters\x18\x02 \x01(\x0b\x32\x16.geocube.RecordFiltersH\x00\x12/\n\x08grecords\x18\n \x01(\x0b\x32\x1b.geocube.GroupedRecordsListH\x00\x12\x14\n\x0cinstances_id\x18\x03 \x03(\t\x12\x0b\n\x03\x63rs\x18\x04 \x01(\t\x12)\n\npix_to_crs\x18\x05 \x01(\x0b\x32\x15.geocube.GeoTransform\x12\x1b\n\x04size\x18\x06 \x01(\x0b\x32\r.geocube.Size\x12\x19\n\x11\x63ompression_level\x18\x07 \x01(\x05\x12\x14\n\x0cheaders_only\x18\x08 \x01(\x08\x12#\n\x06\x66ormat\x18\t \x01(\x0e\x32\x13.geocube.FileFormatB\x10\n\x0erecords_lister\";\n\x15GetCubeResponseHeader\x12\r\n\x05\x63ount\x18\x01 \x01(\x03\x12\x13\n\x0bnb_datasets\x18\x02 \x01(\x03\"\xa4\x01\n\x0fGetCubeResponse\x12\x37\n\rglobal_header\x18\x03 \x01(\x0b\x32\x1e.geocube.GetCubeResponseHeaderH\x00\x12&\n\x06header\x18\x01 \x01(\x0b\x32\x14.geocube.ImageHeaderH\x00\x12$\n\x05\x63hunk\x18\x02 \x01(\x0b\x32\x13.geocube.ImageChunkH\x00\x42\n\n\x08response\"\x80\x01\n\x0eGetTileRequest\x12\x13\n\x0binstance_id\x18\x01 \x01(\t\x12\t\n\x01x\x18\x02 \x01(\x05\x12\t\n\x01y\x18\x03 \x01(\x05\x12\t\n\x01z\x18\x04 \x01(\x05\x12&\n\x07records\x18\x05 \x01(\x0b\x32\x13.geocube.RecordListH\x00\x42\x10\n\x0erecords_lister\"4\n\x0fGetTileResponse\x12!\n\x05image\x18\x01 \x01(\x0b\x32\x12.geocube.ImageFile*,\n\tByteOrder\x12\x10\n\x0cLittleEndian\x10\x00\x12\r\n\tBigEndian\x10\x01* \n\nFileFormat\x12\x07\n\x03Raw\x10\x00\x12\t\n\x05GTiff\x10\x01\x42\x0eZ\x0c./pb;geocubeb\x06proto3'
  ,
  dependencies=[geocube_dot_pb_dot_dataformat__pb2.DESCRIPTOR,geocube_dot_pb_dot_records__pb2.DESCRIPTOR,geocube_dot_pb_dot_layouts__pb2.DESCRIPTOR,])

_BYTEORDER = _descriptor.EnumDescriptor(
  name='ByteOrder',
  full_name='geocube.ByteOrder',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LittleEndian', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BigEndian', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1253,
  serialized_end=1297,
)
_sym_db.RegisterEnumDescriptor(_BYTEORDER)

ByteOrder = enum_type_wrapper.EnumTypeWrapper(_BYTEORDER)
_FILEFORMAT = _descriptor.EnumDescriptor(
  name='FileFormat',
  full_name='geocube.FileFormat',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Raw', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GTiff', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1299,
  serialized_end=1331,
)
_sym_db.RegisterEnumDescriptor(_FILEFORMAT)

FileFormat = enum_type_wrapper.EnumTypeWrapper(_FILEFORMAT)
LittleEndian = 0
BigEndian = 1
Raw = 0
GTiff = 1



_SHAPE = _descriptor.Descriptor(
  name='Shape',
  full_name='geocube.Shape',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dim1', full_name='geocube.Shape.dim1', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dim2', full_name='geocube.Shape.dim2', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dim3', full_name='geocube.Shape.dim3', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=118,
  serialized_end=167,
)


_IMAGEHEADER = _descriptor.Descriptor(
  name='ImageHeader',
  full_name='geocube.ImageHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='geocube.ImageHeader.shape', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='geocube.ImageHeader.dtype', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='geocube.ImageHeader.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nb_parts', full_name='geocube.ImageHeader.nb_parts', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='geocube.ImageHeader.size', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='geocube.ImageHeader.order', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compression', full_name='geocube.ImageHeader.compression', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='records', full_name='geocube.ImageHeader.records', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='geocube.ImageHeader.error', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=170,
  serialized_end=407,
)


_IMAGECHUNK = _descriptor.Descriptor(
  name='ImageChunk',
  full_name='geocube.ImageChunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='part', full_name='geocube.ImageChunk.part', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='geocube.ImageChunk.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=409,
  serialized_end=449,
)


_IMAGEFILE = _descriptor.Descriptor(
  name='ImageFile',
  full_name='geocube.ImageFile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='geocube.ImageFile.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=451,
  serialized_end=476,
)


_GETCUBEREQUEST = _descriptor.Descriptor(
  name='GetCubeRequest',
  full_name='geocube.GetCubeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='records', full_name='geocube.GetCubeRequest.records', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filters', full_name='geocube.GetCubeRequest.filters', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='grecords', full_name='geocube.GetCubeRequest.grecords', index=2,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instances_id', full_name='geocube.GetCubeRequest.instances_id', index=3,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crs', full_name='geocube.GetCubeRequest.crs', index=4,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pix_to_crs', full_name='geocube.GetCubeRequest.pix_to_crs', index=5,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='geocube.GetCubeRequest.size', index=6,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compression_level', full_name='geocube.GetCubeRequest.compression_level', index=7,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='headers_only', full_name='geocube.GetCubeRequest.headers_only', index=8,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='format', full_name='geocube.GetCubeRequest.format', index=9,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='records_lister', full_name='geocube.GetCubeRequest.records_lister',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=479,
  serialized_end=838,
)


_GETCUBERESPONSEHEADER = _descriptor.Descriptor(
  name='GetCubeResponseHeader',
  full_name='geocube.GetCubeResponseHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='geocube.GetCubeResponseHeader.count', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nb_datasets', full_name='geocube.GetCubeResponseHeader.nb_datasets', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=840,
  serialized_end=899,
)


_GETCUBERESPONSE = _descriptor.Descriptor(
  name='GetCubeResponse',
  full_name='geocube.GetCubeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='global_header', full_name='geocube.GetCubeResponse.global_header', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='geocube.GetCubeResponse.header', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunk', full_name='geocube.GetCubeResponse.chunk', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='response', full_name='geocube.GetCubeResponse.response',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=902,
  serialized_end=1066,
)


_GETTILEREQUEST = _descriptor.Descriptor(
  name='GetTileRequest',
  full_name='geocube.GetTileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='geocube.GetTileRequest.instance_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x', full_name='geocube.GetTileRequest.x', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='geocube.GetTileRequest.y', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='z', full_name='geocube.GetTileRequest.z', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='records', full_name='geocube.GetTileRequest.records', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='records_lister', full_name='geocube.GetTileRequest.records_lister',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1069,
  serialized_end=1197,
)


_GETTILERESPONSE = _descriptor.Descriptor(
  name='GetTileResponse',
  full_name='geocube.GetTileResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='geocube.GetTileResponse.image', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1199,
  serialized_end=1251,
)

_IMAGEHEADER.fields_by_name['shape'].message_type = _SHAPE
_IMAGEHEADER.fields_by_name['dtype'].enum_type = geocube_dot_pb_dot_dataformat__pb2._DATAFORMAT_DTYPE
_IMAGEHEADER.fields_by_name['order'].enum_type = _BYTEORDER
_IMAGEHEADER.fields_by_name['records'].message_type = geocube_dot_pb_dot_records__pb2._RECORD
_GETCUBEREQUEST.fields_by_name['records'].message_type = geocube_dot_pb_dot_records__pb2._RECORDLIST
_GETCUBEREQUEST.fields_by_name['filters'].message_type = geocube_dot_pb_dot_records__pb2._RECORDFILTERS
_GETCUBEREQUEST.fields_by_name['grecords'].message_type = geocube_dot_pb_dot_records__pb2._GROUPEDRECORDSLIST
_GETCUBEREQUEST.fields_by_name['pix_to_crs'].message_type = geocube_dot_pb_dot_layouts__pb2._GEOTRANSFORM
_GETCUBEREQUEST.fields_by_name['size'].message_type = geocube_dot_pb_dot_layouts__pb2._SIZE
_GETCUBEREQUEST.fields_by_name['format'].enum_type = _FILEFORMAT
_GETCUBEREQUEST.oneofs_by_name['records_lister'].fields.append(
  _GETCUBEREQUEST.fields_by_name['records'])
_GETCUBEREQUEST.fields_by_name['records'].containing_oneof = _GETCUBEREQUEST.oneofs_by_name['records_lister']
_GETCUBEREQUEST.oneofs_by_name['records_lister'].fields.append(
  _GETCUBEREQUEST.fields_by_name['filters'])
_GETCUBEREQUEST.fields_by_name['filters'].containing_oneof = _GETCUBEREQUEST.oneofs_by_name['records_lister']
_GETCUBEREQUEST.oneofs_by_name['records_lister'].fields.append(
  _GETCUBEREQUEST.fields_by_name['grecords'])
_GETCUBEREQUEST.fields_by_name['grecords'].containing_oneof = _GETCUBEREQUEST.oneofs_by_name['records_lister']
_GETCUBERESPONSE.fields_by_name['global_header'].message_type = _GETCUBERESPONSEHEADER
_GETCUBERESPONSE.fields_by_name['header'].message_type = _IMAGEHEADER
_GETCUBERESPONSE.fields_by_name['chunk'].message_type = _IMAGECHUNK
_GETCUBERESPONSE.oneofs_by_name['response'].fields.append(
  _GETCUBERESPONSE.fields_by_name['global_header'])
_GETCUBERESPONSE.fields_by_name['global_header'].containing_oneof = _GETCUBERESPONSE.oneofs_by_name['response']
_GETCUBERESPONSE.oneofs_by_name['response'].fields.append(
  _GETCUBERESPONSE.fields_by_name['header'])
_GETCUBERESPONSE.fields_by_name['header'].containing_oneof = _GETCUBERESPONSE.oneofs_by_name['response']
_GETCUBERESPONSE.oneofs_by_name['response'].fields.append(
  _GETCUBERESPONSE.fields_by_name['chunk'])
_GETCUBERESPONSE.fields_by_name['chunk'].containing_oneof = _GETCUBERESPONSE.oneofs_by_name['response']
_GETTILEREQUEST.fields_by_name['records'].message_type = geocube_dot_pb_dot_records__pb2._RECORDLIST
_GETTILEREQUEST.oneofs_by_name['records_lister'].fields.append(
  _GETTILEREQUEST.fields_by_name['records'])
_GETTILEREQUEST.fields_by_name['records'].containing_oneof = _GETTILEREQUEST.oneofs_by_name['records_lister']
_GETTILERESPONSE.fields_by_name['image'].message_type = _IMAGEFILE
DESCRIPTOR.message_types_by_name['Shape'] = _SHAPE
DESCRIPTOR.message_types_by_name['ImageHeader'] = _IMAGEHEADER
DESCRIPTOR.message_types_by_name['ImageChunk'] = _IMAGECHUNK
DESCRIPTOR.message_types_by_name['ImageFile'] = _IMAGEFILE
DESCRIPTOR.message_types_by_name['GetCubeRequest'] = _GETCUBEREQUEST
DESCRIPTOR.message_types_by_name['GetCubeResponseHeader'] = _GETCUBERESPONSEHEADER
DESCRIPTOR.message_types_by_name['GetCubeResponse'] = _GETCUBERESPONSE
DESCRIPTOR.message_types_by_name['GetTileRequest'] = _GETTILEREQUEST
DESCRIPTOR.message_types_by_name['GetTileResponse'] = _GETTILERESPONSE
DESCRIPTOR.enum_types_by_name['ByteOrder'] = _BYTEORDER
DESCRIPTOR.enum_types_by_name['FileFormat'] = _FILEFORMAT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Shape = _reflection.GeneratedProtocolMessageType('Shape', (_message.Message,), {
  'DESCRIPTOR' : _SHAPE,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.Shape)
  })
_sym_db.RegisterMessage(Shape)

ImageHeader = _reflection.GeneratedProtocolMessageType('ImageHeader', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEHEADER,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ImageHeader)
  })
_sym_db.RegisterMessage(ImageHeader)

ImageChunk = _reflection.GeneratedProtocolMessageType('ImageChunk', (_message.Message,), {
  'DESCRIPTOR' : _IMAGECHUNK,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ImageChunk)
  })
_sym_db.RegisterMessage(ImageChunk)

ImageFile = _reflection.GeneratedProtocolMessageType('ImageFile', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEFILE,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ImageFile)
  })
_sym_db.RegisterMessage(ImageFile)

GetCubeRequest = _reflection.GeneratedProtocolMessageType('GetCubeRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCUBEREQUEST,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetCubeRequest)
  })
_sym_db.RegisterMessage(GetCubeRequest)

GetCubeResponseHeader = _reflection.GeneratedProtocolMessageType('GetCubeResponseHeader', (_message.Message,), {
  'DESCRIPTOR' : _GETCUBERESPONSEHEADER,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetCubeResponseHeader)
  })
_sym_db.RegisterMessage(GetCubeResponseHeader)

GetCubeResponse = _reflection.GeneratedProtocolMessageType('GetCubeResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCUBERESPONSE,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetCubeResponse)
  })
_sym_db.RegisterMessage(GetCubeResponse)

GetTileRequest = _reflection.GeneratedProtocolMessageType('GetTileRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETTILEREQUEST,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetTileRequest)
  })
_sym_db.RegisterMessage(GetTileRequest)

GetTileResponse = _reflection.GeneratedProtocolMessageType('GetTileResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETTILERESPONSE,
  '__module__' : 'geocube.pb.catalog_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetTileResponse)
  })
_sym_db.RegisterMessage(GetTileResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
