# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: absolute_skew_deviation.proto
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
    'absolute_skew_deviation.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x61\x62solute_skew_deviation.proto\x12\x17\x61\x62solute_skew_deviation\"@\n\x1c\x41\x62soluteSkewDeviationRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x10\n\x08lookback\x18\x02 \x01(\x05\"/\n\x1d\x41\x62soluteSkewDeviationResponse\x12\x0e\n\x06series\x18\x01 \x01(\x0c\x32\xaa\x01\n\x1c\x41\x62soluteSkewDeviationService\x12\x89\x01\n\x18GetAbsoluteSkewDeviation\x12\x35.absolute_skew_deviation.AbsoluteSkewDeviationRequest\x1a\x36.absolute_skew_deviation.AbsoluteSkewDeviationResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'absolute_skew_deviation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ABSOLUTESKEWDEVIATIONREQUEST']._serialized_start=58
  _globals['_ABSOLUTESKEWDEVIATIONREQUEST']._serialized_end=122
  _globals['_ABSOLUTESKEWDEVIATIONRESPONSE']._serialized_start=124
  _globals['_ABSOLUTESKEWDEVIATIONRESPONSE']._serialized_end=171
  _globals['_ABSOLUTESKEWDEVIATIONSERVICE']._serialized_start=174
  _globals['_ABSOLUTESKEWDEVIATIONSERVICE']._serialized_end=344
# @@protoc_insertion_point(module_scope)
