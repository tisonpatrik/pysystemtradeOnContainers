# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: accel.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'accel.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61\x63\x63\x65l.proto\x12\x05rules\"t\n\x0c\x41\x63\x63\x65lRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\r\n\x05lfast\x18\x02 \x01(\x05\x12\x17\n\x0fuse_attenuation\x18\x03 \x01(\x08\x12\x16\n\x0escaling_factor\x18\x04 \x01(\x02\x12\x14\n\x0cscaling_type\x18\x05 \x01(\t\"\x1f\n\rAccelResponse\x12\x0e\n\x06series\x18\x01 \x01(\x0c\x32?\n\x05\x41\x63\x63\x65l\x12\x36\n\tget_accel\x12\x13.rules.AccelRequest\x1a\x14.rules.AccelResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'accel_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ACCELREQUEST']._serialized_start=22
  _globals['_ACCELREQUEST']._serialized_end=138
  _globals['_ACCELRESPONSE']._serialized_start=140
  _globals['_ACCELRESPONSE']._serialized_end=171
  _globals['_ACCEL']._serialized_start=173
  _globals['_ACCEL']._serialized_end=236
# @@protoc_insertion_point(module_scope)
