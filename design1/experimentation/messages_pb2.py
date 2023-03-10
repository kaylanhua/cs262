# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='messages',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0emessages.proto\x12\x08messages\"T\n\x0fMessageToServer\x12\x0e\n\x06opcode\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x05 \x01(\t\x12\x0e\n\x06target\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\"\x1c\n\tServerLog\x12\x0f\n\x07message\x18\x01 \x01(\t2V\n\x06Server\x12L\n\x18ReceiveMessageFromClient\x12\x19.messages.MessageToServer\x1a\x13.messages.ServerLog\"\x00\x62\x06proto3')
)




_MESSAGETOSERVER = _descriptor.Descriptor(
  name='MessageToServer',
  full_name='messages.MessageToServer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opcode', full_name='messages.MessageToServer.opcode', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='username', full_name='messages.MessageToServer.username', index=1,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target', full_name='messages.MessageToServer.target', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='messages.MessageToServer.message', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=28,
  serialized_end=112,
)


_SERVERLOG = _descriptor.Descriptor(
  name='ServerLog',
  full_name='messages.ServerLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='messages.ServerLog.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=114,
  serialized_end=142,
)

DESCRIPTOR.message_types_by_name['MessageToServer'] = _MESSAGETOSERVER
DESCRIPTOR.message_types_by_name['ServerLog'] = _SERVERLOG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageToServer = _reflection.GeneratedProtocolMessageType('MessageToServer', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGETOSERVER,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:messages.MessageToServer)
  ))
_sym_db.RegisterMessage(MessageToServer)

ServerLog = _reflection.GeneratedProtocolMessageType('ServerLog', (_message.Message,), dict(
  DESCRIPTOR = _SERVERLOG,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:messages.ServerLog)
  ))
_sym_db.RegisterMessage(ServerLog)



_SERVER = _descriptor.ServiceDescriptor(
  name='Server',
  full_name='messages.Server',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=144,
  serialized_end=230,
  methods=[
  _descriptor.MethodDescriptor(
    name='ReceiveMessageFromClient',
    full_name='messages.Server.ReceiveMessageFromClient',
    index=0,
    containing_service=None,
    input_type=_MESSAGETOSERVER,
    output_type=_SERVERLOG,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVER)

DESCRIPTOR.services_by_name['Server'] = _SERVER

# @@protoc_insertion_point(module_scope)
