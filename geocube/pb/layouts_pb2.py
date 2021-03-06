# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/layouts.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from geocube.pb import records_pb2 as geocube_dot_pb_dot_records__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='geocube/pb/layouts.proto',
  package='geocube',
  syntax='proto3',
  serialized_options=b'Z\014./pb;geocube',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18geocube/pb/layouts.proto\x12\x07geocube\x1a\x18geocube/pb/records.proto\"%\n\x04Size\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05\"P\n\x0cGeoTransform\x12\t\n\x01\x61\x18\x01 \x01(\x01\x12\t\n\x01\x62\x18\x02 \x01(\x01\x12\t\n\x01\x63\x18\x03 \x01(\x01\x12\t\n\x01\x64\x18\x04 \x01(\x01\x12\t\n\x01\x65\x18\x05 \x01(\x01\x12\t\n\x01\x66\x18\x06 \x01(\x01\"]\n\x04Tile\x12(\n\ttransform\x18\x01 \x01(\x0b\x32\x15.geocube.GeoTransform\x12\x1e\n\x07size_px\x18\x02 \x01(\x0b\x32\r.geocube.Size\x12\x0b\n\x03\x63rs\x18\x03 \x01(\t\"\xe0\x01\n\x06Layout\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\ngrid_flags\x18\x03 \x03(\t\x12<\n\x0fgrid_parameters\x18\x04 \x03(\x0b\x32#.geocube.Layout.GridParametersEntry\x12\x14\n\x0c\x62lock_x_size\x18\x05 \x01(\x03\x12\x14\n\x0c\x62lock_y_size\x18\x06 \x01(\x03\x12\x13\n\x0bmax_records\x18\x07 \x01(\x03\x1a\x35\n\x13GridParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"6\n\x13\x43reateLayoutRequest\x12\x1f\n\x06layout\x18\x01 \x01(\x0b\x32\x0f.geocube.Layout\"\x16\n\x14\x43reateLayoutResponse\"#\n\x13\x44\x65leteLayoutRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x16\n\x14\x44\x65leteLayoutResponse\"\'\n\x12ListLayoutsRequest\x12\x11\n\tname_like\x18\x01 \x01(\t\"7\n\x13ListLayoutsResponse\x12 \n\x07layouts\x18\x01 \x03(\x0b\x32\x0f.geocube.Layout\"s\n\x0eTileAOIRequest\x12\x19\n\x03\x61oi\x18\x01 \x01(\x0b\x32\x0c.geocube.AOI\x12\x15\n\x0blayout_name\x18\x05 \x01(\tH\x00\x12!\n\x06layout\x18\x06 \x01(\x0b\x32\x0f.geocube.LayoutH\x00\x42\x0c\n\nidentifier\"/\n\x0fTileAOIResponse\x12\x1c\n\x05tiles\x18\x01 \x03(\x0b\x32\r.geocube.Tile\"G\n\x04Grid\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x1c\n\x05\x63\x65lls\x18\x03 \x03(\x0b\x32\r.geocube.Cell\"I\n\x04\x43\x65ll\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0b\n\x03\x63rs\x18\x02 \x01(\t\x12(\n\x0b\x63oordinates\x18\x03 \x01(\x0b\x32\x13.geocube.LinearRing\"0\n\x11\x43reateGridRequest\x12\x1b\n\x04grid\x18\x01 \x01(\x0b\x32\r.geocube.Grid\"\x14\n\x12\x43reateGridResponse\"!\n\x11\x44\x65leteGridRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x14\n\x12\x44\x65leteGridResponse\"%\n\x10ListGridsRequest\x12\x11\n\tname_like\x18\x01 \x01(\t\"1\n\x11ListGridsResponse\x12\x1c\n\x05grids\x18\x01 \x03(\x0b\x32\r.geocube.GridB\x0eZ\x0c./pb;geocubeb\x06proto3'
  ,
  dependencies=[geocube_dot_pb_dot_records__pb2.DESCRIPTOR,])




_SIZE = _descriptor.Descriptor(
  name='Size',
  full_name='geocube.Size',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='geocube.Size.width', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='geocube.Size.height', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=63,
  serialized_end=100,
)


_GEOTRANSFORM = _descriptor.Descriptor(
  name='GeoTransform',
  full_name='geocube.GeoTransform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='geocube.GeoTransform.a', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='b', full_name='geocube.GeoTransform.b', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='c', full_name='geocube.GeoTransform.c', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='d', full_name='geocube.GeoTransform.d', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='e', full_name='geocube.GeoTransform.e', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='f', full_name='geocube.GeoTransform.f', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=102,
  serialized_end=182,
)


_TILE = _descriptor.Descriptor(
  name='Tile',
  full_name='geocube.Tile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transform', full_name='geocube.Tile.transform', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size_px', full_name='geocube.Tile.size_px', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crs', full_name='geocube.Tile.crs', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=184,
  serialized_end=277,
)


_LAYOUT_GRIDPARAMETERSENTRY = _descriptor.Descriptor(
  name='GridParametersEntry',
  full_name='geocube.Layout.GridParametersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='geocube.Layout.GridParametersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='geocube.Layout.GridParametersEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=451,
  serialized_end=504,
)

_LAYOUT = _descriptor.Descriptor(
  name='Layout',
  full_name='geocube.Layout',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geocube.Layout.name', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='grid_flags', full_name='geocube.Layout.grid_flags', index=1,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='grid_parameters', full_name='geocube.Layout.grid_parameters', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block_x_size', full_name='geocube.Layout.block_x_size', index=3,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block_y_size', full_name='geocube.Layout.block_y_size', index=4,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_records', full_name='geocube.Layout.max_records', index=5,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_LAYOUT_GRIDPARAMETERSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=280,
  serialized_end=504,
)


_CREATELAYOUTREQUEST = _descriptor.Descriptor(
  name='CreateLayoutRequest',
  full_name='geocube.CreateLayoutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='layout', full_name='geocube.CreateLayoutRequest.layout', index=0,
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
  serialized_start=506,
  serialized_end=560,
)


_CREATELAYOUTRESPONSE = _descriptor.Descriptor(
  name='CreateLayoutResponse',
  full_name='geocube.CreateLayoutResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=562,
  serialized_end=584,
)


_DELETELAYOUTREQUEST = _descriptor.Descriptor(
  name='DeleteLayoutRequest',
  full_name='geocube.DeleteLayoutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geocube.DeleteLayoutRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=586,
  serialized_end=621,
)


_DELETELAYOUTRESPONSE = _descriptor.Descriptor(
  name='DeleteLayoutResponse',
  full_name='geocube.DeleteLayoutResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=623,
  serialized_end=645,
)


_LISTLAYOUTSREQUEST = _descriptor.Descriptor(
  name='ListLayoutsRequest',
  full_name='geocube.ListLayoutsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name_like', full_name='geocube.ListLayoutsRequest.name_like', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=647,
  serialized_end=686,
)


_LISTLAYOUTSRESPONSE = _descriptor.Descriptor(
  name='ListLayoutsResponse',
  full_name='geocube.ListLayoutsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='layouts', full_name='geocube.ListLayoutsResponse.layouts', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=688,
  serialized_end=743,
)


_TILEAOIREQUEST = _descriptor.Descriptor(
  name='TileAOIRequest',
  full_name='geocube.TileAOIRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='aoi', full_name='geocube.TileAOIRequest.aoi', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='layout_name', full_name='geocube.TileAOIRequest.layout_name', index=1,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='layout', full_name='geocube.TileAOIRequest.layout', index=2,
      number=6, type=11, cpp_type=10, label=1,
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
      name='identifier', full_name='geocube.TileAOIRequest.identifier',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=745,
  serialized_end=860,
)


_TILEAOIRESPONSE = _descriptor.Descriptor(
  name='TileAOIResponse',
  full_name='geocube.TileAOIResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tiles', full_name='geocube.TileAOIResponse.tiles', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=862,
  serialized_end=909,
)


_GRID = _descriptor.Descriptor(
  name='Grid',
  full_name='geocube.Grid',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geocube.Grid.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='geocube.Grid.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cells', full_name='geocube.Grid.cells', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=911,
  serialized_end=982,
)


_CELL = _descriptor.Descriptor(
  name='Cell',
  full_name='geocube.Cell',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='geocube.Cell.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crs', full_name='geocube.Cell.crs', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='coordinates', full_name='geocube.Cell.coordinates', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=984,
  serialized_end=1057,
)


_CREATEGRIDREQUEST = _descriptor.Descriptor(
  name='CreateGridRequest',
  full_name='geocube.CreateGridRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='grid', full_name='geocube.CreateGridRequest.grid', index=0,
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
  serialized_start=1059,
  serialized_end=1107,
)


_CREATEGRIDRESPONSE = _descriptor.Descriptor(
  name='CreateGridResponse',
  full_name='geocube.CreateGridResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1109,
  serialized_end=1129,
)


_DELETEGRIDREQUEST = _descriptor.Descriptor(
  name='DeleteGridRequest',
  full_name='geocube.DeleteGridRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='geocube.DeleteGridRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=1131,
  serialized_end=1164,
)


_DELETEGRIDRESPONSE = _descriptor.Descriptor(
  name='DeleteGridResponse',
  full_name='geocube.DeleteGridResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1166,
  serialized_end=1186,
)


_LISTGRIDSREQUEST = _descriptor.Descriptor(
  name='ListGridsRequest',
  full_name='geocube.ListGridsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name_like', full_name='geocube.ListGridsRequest.name_like', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=1188,
  serialized_end=1225,
)


_LISTGRIDSRESPONSE = _descriptor.Descriptor(
  name='ListGridsResponse',
  full_name='geocube.ListGridsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='grids', full_name='geocube.ListGridsResponse.grids', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1227,
  serialized_end=1276,
)

_TILE.fields_by_name['transform'].message_type = _GEOTRANSFORM
_TILE.fields_by_name['size_px'].message_type = _SIZE
_LAYOUT_GRIDPARAMETERSENTRY.containing_type = _LAYOUT
_LAYOUT.fields_by_name['grid_parameters'].message_type = _LAYOUT_GRIDPARAMETERSENTRY
_CREATELAYOUTREQUEST.fields_by_name['layout'].message_type = _LAYOUT
_LISTLAYOUTSRESPONSE.fields_by_name['layouts'].message_type = _LAYOUT
_TILEAOIREQUEST.fields_by_name['aoi'].message_type = geocube_dot_pb_dot_records__pb2._AOI
_TILEAOIREQUEST.fields_by_name['layout'].message_type = _LAYOUT
_TILEAOIREQUEST.oneofs_by_name['identifier'].fields.append(
  _TILEAOIREQUEST.fields_by_name['layout_name'])
_TILEAOIREQUEST.fields_by_name['layout_name'].containing_oneof = _TILEAOIREQUEST.oneofs_by_name['identifier']
_TILEAOIREQUEST.oneofs_by_name['identifier'].fields.append(
  _TILEAOIREQUEST.fields_by_name['layout'])
_TILEAOIREQUEST.fields_by_name['layout'].containing_oneof = _TILEAOIREQUEST.oneofs_by_name['identifier']
_TILEAOIRESPONSE.fields_by_name['tiles'].message_type = _TILE
_GRID.fields_by_name['cells'].message_type = _CELL
_CELL.fields_by_name['coordinates'].message_type = geocube_dot_pb_dot_records__pb2._LINEARRING
_CREATEGRIDREQUEST.fields_by_name['grid'].message_type = _GRID
_LISTGRIDSRESPONSE.fields_by_name['grids'].message_type = _GRID
DESCRIPTOR.message_types_by_name['Size'] = _SIZE
DESCRIPTOR.message_types_by_name['GeoTransform'] = _GEOTRANSFORM
DESCRIPTOR.message_types_by_name['Tile'] = _TILE
DESCRIPTOR.message_types_by_name['Layout'] = _LAYOUT
DESCRIPTOR.message_types_by_name['CreateLayoutRequest'] = _CREATELAYOUTREQUEST
DESCRIPTOR.message_types_by_name['CreateLayoutResponse'] = _CREATELAYOUTRESPONSE
DESCRIPTOR.message_types_by_name['DeleteLayoutRequest'] = _DELETELAYOUTREQUEST
DESCRIPTOR.message_types_by_name['DeleteLayoutResponse'] = _DELETELAYOUTRESPONSE
DESCRIPTOR.message_types_by_name['ListLayoutsRequest'] = _LISTLAYOUTSREQUEST
DESCRIPTOR.message_types_by_name['ListLayoutsResponse'] = _LISTLAYOUTSRESPONSE
DESCRIPTOR.message_types_by_name['TileAOIRequest'] = _TILEAOIREQUEST
DESCRIPTOR.message_types_by_name['TileAOIResponse'] = _TILEAOIRESPONSE
DESCRIPTOR.message_types_by_name['Grid'] = _GRID
DESCRIPTOR.message_types_by_name['Cell'] = _CELL
DESCRIPTOR.message_types_by_name['CreateGridRequest'] = _CREATEGRIDREQUEST
DESCRIPTOR.message_types_by_name['CreateGridResponse'] = _CREATEGRIDRESPONSE
DESCRIPTOR.message_types_by_name['DeleteGridRequest'] = _DELETEGRIDREQUEST
DESCRIPTOR.message_types_by_name['DeleteGridResponse'] = _DELETEGRIDRESPONSE
DESCRIPTOR.message_types_by_name['ListGridsRequest'] = _LISTGRIDSREQUEST
DESCRIPTOR.message_types_by_name['ListGridsResponse'] = _LISTGRIDSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Size = _reflection.GeneratedProtocolMessageType('Size', (_message.Message,), {
  'DESCRIPTOR' : _SIZE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.Size)
  })
_sym_db.RegisterMessage(Size)

GeoTransform = _reflection.GeneratedProtocolMessageType('GeoTransform', (_message.Message,), {
  'DESCRIPTOR' : _GEOTRANSFORM,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GeoTransform)
  })
_sym_db.RegisterMessage(GeoTransform)

Tile = _reflection.GeneratedProtocolMessageType('Tile', (_message.Message,), {
  'DESCRIPTOR' : _TILE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.Tile)
  })
_sym_db.RegisterMessage(Tile)

Layout = _reflection.GeneratedProtocolMessageType('Layout', (_message.Message,), {

  'GridParametersEntry' : _reflection.GeneratedProtocolMessageType('GridParametersEntry', (_message.Message,), {
    'DESCRIPTOR' : _LAYOUT_GRIDPARAMETERSENTRY,
    '__module__' : 'geocube.pb.layouts_pb2'
    # @@protoc_insertion_point(class_scope:geocube.Layout.GridParametersEntry)
    })
  ,
  'DESCRIPTOR' : _LAYOUT,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.Layout)
  })
_sym_db.RegisterMessage(Layout)
_sym_db.RegisterMessage(Layout.GridParametersEntry)

CreateLayoutRequest = _reflection.GeneratedProtocolMessageType('CreateLayoutRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATELAYOUTREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.CreateLayoutRequest)
  })
_sym_db.RegisterMessage(CreateLayoutRequest)

CreateLayoutResponse = _reflection.GeneratedProtocolMessageType('CreateLayoutResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATELAYOUTRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.CreateLayoutResponse)
  })
_sym_db.RegisterMessage(CreateLayoutResponse)

DeleteLayoutRequest = _reflection.GeneratedProtocolMessageType('DeleteLayoutRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETELAYOUTREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.DeleteLayoutRequest)
  })
_sym_db.RegisterMessage(DeleteLayoutRequest)

DeleteLayoutResponse = _reflection.GeneratedProtocolMessageType('DeleteLayoutResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETELAYOUTRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.DeleteLayoutResponse)
  })
_sym_db.RegisterMessage(DeleteLayoutResponse)

ListLayoutsRequest = _reflection.GeneratedProtocolMessageType('ListLayoutsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTLAYOUTSREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ListLayoutsRequest)
  })
_sym_db.RegisterMessage(ListLayoutsRequest)

ListLayoutsResponse = _reflection.GeneratedProtocolMessageType('ListLayoutsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTLAYOUTSRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ListLayoutsResponse)
  })
_sym_db.RegisterMessage(ListLayoutsResponse)

TileAOIRequest = _reflection.GeneratedProtocolMessageType('TileAOIRequest', (_message.Message,), {
  'DESCRIPTOR' : _TILEAOIREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.TileAOIRequest)
  })
_sym_db.RegisterMessage(TileAOIRequest)

TileAOIResponse = _reflection.GeneratedProtocolMessageType('TileAOIResponse', (_message.Message,), {
  'DESCRIPTOR' : _TILEAOIRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.TileAOIResponse)
  })
_sym_db.RegisterMessage(TileAOIResponse)

Grid = _reflection.GeneratedProtocolMessageType('Grid', (_message.Message,), {
  'DESCRIPTOR' : _GRID,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.Grid)
  })
_sym_db.RegisterMessage(Grid)

Cell = _reflection.GeneratedProtocolMessageType('Cell', (_message.Message,), {
  'DESCRIPTOR' : _CELL,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.Cell)
  })
_sym_db.RegisterMessage(Cell)

CreateGridRequest = _reflection.GeneratedProtocolMessageType('CreateGridRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEGRIDREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.CreateGridRequest)
  })
_sym_db.RegisterMessage(CreateGridRequest)

CreateGridResponse = _reflection.GeneratedProtocolMessageType('CreateGridResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEGRIDRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.CreateGridResponse)
  })
_sym_db.RegisterMessage(CreateGridResponse)

DeleteGridRequest = _reflection.GeneratedProtocolMessageType('DeleteGridRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEGRIDREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.DeleteGridRequest)
  })
_sym_db.RegisterMessage(DeleteGridRequest)

DeleteGridResponse = _reflection.GeneratedProtocolMessageType('DeleteGridResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEGRIDRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.DeleteGridResponse)
  })
_sym_db.RegisterMessage(DeleteGridResponse)

ListGridsRequest = _reflection.GeneratedProtocolMessageType('ListGridsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTGRIDSREQUEST,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ListGridsRequest)
  })
_sym_db.RegisterMessage(ListGridsRequest)

ListGridsResponse = _reflection.GeneratedProtocolMessageType('ListGridsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTGRIDSRESPONSE,
  '__module__' : 'geocube.pb.layouts_pb2'
  # @@protoc_insertion_point(class_scope:geocube.ListGridsResponse)
  })
_sym_db.RegisterMessage(ListGridsResponse)


DESCRIPTOR._options = None
_LAYOUT_GRIDPARAMETERSENTRY._options = None
# @@protoc_insertion_point(module_scope)
