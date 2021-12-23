# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/datasetMeta.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from geocube.pb import dataformat_pb2 as geocube_dot_pb_dot_dataformat__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='geocube/pb/datasetMeta.proto',
  package='geocube',
  syntax='proto3',
  serialized_options=b'Z\014./pb;geocube',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1cgeocube/pb/datasetMeta.proto\x12\x07geocube\x1a\x1bgeocube/pb/dataformat.proto\";\n\x0b\x44\x61tasetMeta\x12,\n\rinternalsMeta\x18\x03 \x03(\x0b\x32\x15.geocube.InternalMeta\"\xac\x01\n\x0cInternalMeta\x12\x15\n\rcontainer_uri\x18\x01 \x01(\t\x12\x18\n\x10\x63ontainer_subdir\x18\x02 \x01(\t\x12\r\n\x05\x62\x61nds\x18\x03 \x03(\x03\x12$\n\x07\x64\x66ormat\x18\x04 \x01(\x0b\x32\x13.geocube.DataFormat\x12\x11\n\trange_min\x18\x05 \x01(\x01\x12\x11\n\trange_max\x18\x06 \x01(\x01\x12\x10\n\x08\x65xponent\x18\x07 \x01(\x01\x42\x0eZ\x0c./pb;geocubeb\x06proto3'
  ,
  dependencies=[geocube_dot_pb_dot_dataformat__pb2.DESCRIPTOR,])




_DATASETMETA = _descriptor.Descriptor(
  name='DatasetMeta',
  full_name='geocube.DatasetMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='internalsMeta', full_name='geocube.DatasetMeta.internalsMeta', index=0,
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
  serialized_start=70,
  serialized_end=129,
)


_INTERNALMETA = _descriptor.Descriptor(
  name='InternalMeta',
  full_name='geocube.InternalMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='container_uri', full_name='geocube.InternalMeta.container_uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='container_subdir', full_name='geocube.InternalMeta.container_subdir', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bands', full_name='geocube.InternalMeta.bands', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dformat', full_name='geocube.InternalMeta.dformat', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='range_min', full_name='geocube.InternalMeta.range_min', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='range_max', full_name='geocube.InternalMeta.range_max', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exponent', full_name='geocube.InternalMeta.exponent', index=6,
      number=7, type=1, cpp_type=5, label=1,
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
  serialized_start=132,
  serialized_end=304,
)

_DATASETMETA.fields_by_name['internalsMeta'].message_type = _INTERNALMETA
_INTERNALMETA.fields_by_name['dformat'].message_type = geocube_dot_pb_dot_dataformat__pb2._DATAFORMAT
DESCRIPTOR.message_types_by_name['DatasetMeta'] = _DATASETMETA
DESCRIPTOR.message_types_by_name['InternalMeta'] = _INTERNALMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DatasetMeta = _reflection.GeneratedProtocolMessageType('DatasetMeta', (_message.Message,), {
  'DESCRIPTOR' : _DATASETMETA,
  '__module__' : 'geocube.pb.datasetMeta_pb2'
  # @@protoc_insertion_point(class_scope:geocube.DatasetMeta)
  })
_sym_db.RegisterMessage(DatasetMeta)

InternalMeta = _reflection.GeneratedProtocolMessageType('InternalMeta', (_message.Message,), {
  'DESCRIPTOR' : _INTERNALMETA,
  '__module__' : 'geocube.pb.datasetMeta_pb2'
  # @@protoc_insertion_point(class_scope:geocube.InternalMeta)
  })
_sym_db.RegisterMessage(InternalMeta)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)