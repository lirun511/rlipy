# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SymDataProto.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='SymDataProto.proto',
  package='Core',
  syntax='proto3',
  serialized_pb=_b('\n\x12SymDataProto.proto\x12\x04\x43ore\x1a\x1fgoogle/protobuf/timestamp.proto\".\n\x0bStringField\x12\x11\n\tfieldName\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"+\n\x08IntField\x12\x11\n\tfieldName\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x03\".\n\x0b\x44oubleField\x12\x11\n\tfieldName\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x01\"H\n\tTimeField\x12\x11\n\tfieldName\x18\x01 \x01(\t\x12(\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xb8\x01\n\x0cSymDataProto\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\'\n\x0cstringFields\x18\x02 \x03(\x0b\x32\x11.Core.StringField\x12!\n\tintFields\x18\x03 \x03(\x0b\x32\x0e.Core.IntField\x12\'\n\x0c\x64oubleFields\x18\x04 \x03(\x0b\x32\x11.Core.DoubleField\x12#\n\ntimeFields\x18\x05 \x03(\x0b\x32\x0f.Core.TimeField*S\n\tFieldType\x12\x0e\n\nStringType\x10\x00\x12\x0b\n\x07IntType\x10\x01\x12\x0e\n\nDoubleType\x10\x02\x12\x0c\n\x08TimeType\x10\x03\x12\x0b\n\x07Unknown\x10\x64\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])

_FIELDTYPE = _descriptor.EnumDescriptor(
  name='FieldType',
  full_name='Core.FieldType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='StringType', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IntType', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DoubleType', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TimeType', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Unknown', index=4, number=100,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=463,
  serialized_end=546,
)
_sym_db.RegisterEnumDescriptor(_FIELDTYPE)

FieldType = enum_type_wrapper.EnumTypeWrapper(_FIELDTYPE)
StringType = 0
IntType = 1
DoubleType = 2
TimeType = 3
Unknown = 100



_STRINGFIELD = _descriptor.Descriptor(
  name='StringField',
  full_name='Core.StringField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fieldName', full_name='Core.StringField.fieldName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='Core.StringField.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=107,
)


_INTFIELD = _descriptor.Descriptor(
  name='IntField',
  full_name='Core.IntField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fieldName', full_name='Core.IntField.fieldName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='Core.IntField.data', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=109,
  serialized_end=152,
)


_DOUBLEFIELD = _descriptor.Descriptor(
  name='DoubleField',
  full_name='Core.DoubleField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fieldName', full_name='Core.DoubleField.fieldName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='Core.DoubleField.data', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=200,
)


_TIMEFIELD = _descriptor.Descriptor(
  name='TimeField',
  full_name='Core.TimeField',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fieldName', full_name='Core.TimeField.fieldName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='Core.TimeField.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=202,
  serialized_end=274,
)


_SYMDATAPROTO = _descriptor.Descriptor(
  name='SymDataProto',
  full_name='Core.SymDataProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='Core.SymDataProto.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stringFields', full_name='Core.SymDataProto.stringFields', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intFields', full_name='Core.SymDataProto.intFields', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='doubleFields', full_name='Core.SymDataProto.doubleFields', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeFields', full_name='Core.SymDataProto.timeFields', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=277,
  serialized_end=461,
)

_TIMEFIELD.fields_by_name['data'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_SYMDATAPROTO.fields_by_name['stringFields'].message_type = _STRINGFIELD
_SYMDATAPROTO.fields_by_name['intFields'].message_type = _INTFIELD
_SYMDATAPROTO.fields_by_name['doubleFields'].message_type = _DOUBLEFIELD
_SYMDATAPROTO.fields_by_name['timeFields'].message_type = _TIMEFIELD
DESCRIPTOR.message_types_by_name['StringField'] = _STRINGFIELD
DESCRIPTOR.message_types_by_name['IntField'] = _INTFIELD
DESCRIPTOR.message_types_by_name['DoubleField'] = _DOUBLEFIELD
DESCRIPTOR.message_types_by_name['TimeField'] = _TIMEFIELD
DESCRIPTOR.message_types_by_name['SymDataProto'] = _SYMDATAPROTO
DESCRIPTOR.enum_types_by_name['FieldType'] = _FIELDTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StringField = _reflection.GeneratedProtocolMessageType('StringField', (_message.Message,), dict(
  DESCRIPTOR = _STRINGFIELD,
  __module__ = 'SymDataProto_pb2'
  # @@protoc_insertion_point(class_scope:Core.StringField)
  ))
_sym_db.RegisterMessage(StringField)

IntField = _reflection.GeneratedProtocolMessageType('IntField', (_message.Message,), dict(
  DESCRIPTOR = _INTFIELD,
  __module__ = 'SymDataProto_pb2'
  # @@protoc_insertion_point(class_scope:Core.IntField)
  ))
_sym_db.RegisterMessage(IntField)

DoubleField = _reflection.GeneratedProtocolMessageType('DoubleField', (_message.Message,), dict(
  DESCRIPTOR = _DOUBLEFIELD,
  __module__ = 'SymDataProto_pb2'
  # @@protoc_insertion_point(class_scope:Core.DoubleField)
  ))
_sym_db.RegisterMessage(DoubleField)

TimeField = _reflection.GeneratedProtocolMessageType('TimeField', (_message.Message,), dict(
  DESCRIPTOR = _TIMEFIELD,
  __module__ = 'SymDataProto_pb2'
  # @@protoc_insertion_point(class_scope:Core.TimeField)
  ))
_sym_db.RegisterMessage(TimeField)

SymDataProto = _reflection.GeneratedProtocolMessageType('SymDataProto', (_message.Message,), dict(
  DESCRIPTOR = _SYMDATAPROTO,
  __module__ = 'SymDataProto_pb2'
  # @@protoc_insertion_point(class_scope:Core.SymDataProto)
  ))
_sym_db.RegisterMessage(SymDataProto)


# @@protoc_insertion_point(module_scope)
