# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geocube/pb/version.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='geocube/pb/version.proto',
  package='geocube',
  syntax='proto3',
  serialized_options=b'Z\014./pb;geocube',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18geocube/pb/version.proto\x12\x07geocube\"\x13\n\x11GetVersionRequest\"%\n\x12GetVersionResponse\x12\x0f\n\x07Version\x18\x01 \x01(\tB\x0eZ\x0c./pb;geocubeb\x06proto3'
)




_GETVERSIONREQUEST = _descriptor.Descriptor(
  name='GetVersionRequest',
  full_name='geocube.GetVersionRequest',
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
  serialized_start=37,
  serialized_end=56,
)


_GETVERSIONRESPONSE = _descriptor.Descriptor(
  name='GetVersionResponse',
  full_name='geocube.GetVersionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Version', full_name='geocube.GetVersionResponse.Version', index=0,
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
  serialized_start=58,
  serialized_end=95,
)

DESCRIPTOR.message_types_by_name['GetVersionRequest'] = _GETVERSIONREQUEST
DESCRIPTOR.message_types_by_name['GetVersionResponse'] = _GETVERSIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetVersionRequest = _reflection.GeneratedProtocolMessageType('GetVersionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETVERSIONREQUEST,
  '__module__' : 'geocube.pb.version_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetVersionRequest)
  })
_sym_db.RegisterMessage(GetVersionRequest)

GetVersionResponse = _reflection.GeneratedProtocolMessageType('GetVersionResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETVERSIONRESPONSE,
  '__module__' : 'geocube.pb.version_pb2'
  # @@protoc_insertion_point(class_scope:geocube.GetVersionResponse)
  })
_sym_db.RegisterMessage(GetVersionResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
