# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: smooth_carry.proto
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
    'smooth_carry.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12smooth_carry.proto\x12\x08raw_data\"$\n\x12SmoothCarryRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\"%\n\x13SmoothCarryResponse\x12\x0e\n\x06series\x18\x01 \x01(\x0c\x32^\n\x0bSmoothCarry\x12O\n\x10get_smooth_carry\x12\x1c.raw_data.SmoothCarryRequest\x1a\x1d.raw_data.SmoothCarryResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'smooth_carry_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SMOOTHCARRYREQUEST']._serialized_start=32
  _globals['_SMOOTHCARRYREQUEST']._serialized_end=68
  _globals['_SMOOTHCARRYRESPONSE']._serialized_start=70
  _globals['_SMOOTHCARRYRESPONSE']._serialized_end=107
  _globals['_SMOOTHCARRY']._serialized_start=109
  _globals['_SMOOTHCARRY']._serialized_end=203
# @@protoc_insertion_point(module_scope)
