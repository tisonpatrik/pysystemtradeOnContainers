# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: relative_skew_deviation.proto
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
    'relative_skew_deviation.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1drelative_skew_deviation.proto\x12\x08raw_data\"@\n\x1cRelativeSkewDeviationRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x10\n\x08lookback\x18\x02 \x01(\x05\"/\n\x1dRelativeSkewDeviationResponse\x12\x0e\n\x06series\x18\x01 \x01(\x0c\x32\x87\x01\n\x15RelativeSkewDeviation\x12n\n\x1bget_relative_skew_deviation\x12&.raw_data.RelativeSkewDeviationRequest\x1a\'.raw_data.RelativeSkewDeviationResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'relative_skew_deviation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RELATIVESKEWDEVIATIONREQUEST']._serialized_start=43
  _globals['_RELATIVESKEWDEVIATIONREQUEST']._serialized_end=107
  _globals['_RELATIVESKEWDEVIATIONRESPONSE']._serialized_start=109
  _globals['_RELATIVESKEWDEVIATIONRESPONSE']._serialized_end=156
  _globals['_RELATIVESKEWDEVIATION']._serialized_start=159
  _globals['_RELATIVESKEWDEVIATION']._serialized_end=294
# @@protoc_insertion_point(module_scope)