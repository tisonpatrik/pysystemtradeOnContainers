# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: vol_attenuation.proto
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
    'vol_attenuation.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15vol_attenuation.proto\x12\x08raw_data\"\'\n\x15VolAttenuationRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\"(\n\x16VolAttenuationResponse\x12\x0e\n\x06series\x18\x01 \x01(\x0c\x32j\n\x0eVolAttenuation\x12X\n\x13get_vol_attenuation\x12\x1f.raw_data.VolAttenuationRequest\x1a .raw_data.VolAttenuationResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'vol_attenuation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VOLATTENUATIONREQUEST']._serialized_start=35
  _globals['_VOLATTENUATIONREQUEST']._serialized_end=74
  _globals['_VOLATTENUATIONRESPONSE']._serialized_start=76
  _globals['_VOLATTENUATIONRESPONSE']._serialized_end=116
  _globals['_VOLATTENUATION']._serialized_start=118
  _globals['_VOLATTENUATION']._serialized_end=224
# @@protoc_insertion_point(module_scope)
