# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fx_prices.proto
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
    'fx_prices.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x66x_prices.proto\x12\x17\x61\x62solute_skew_deviation\"8\n\x0f\x46xPricesRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x15\n\rbase_currency\x18\x02 \x01(\t\"\"\n\x10\x46xPricesResponse\x12\x0e\n\x06series\x18\x01 \x01(\x0c\x32w\n\x0f\x46xPricesHandler\x12\x64\n\rget_fx_prices\x12(.absolute_skew_deviation.FxPricesRequest\x1a).absolute_skew_deviation.FxPricesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fx_prices_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FXPRICESREQUEST']._serialized_start=44
  _globals['_FXPRICESREQUEST']._serialized_end=100
  _globals['_FXPRICESRESPONSE']._serialized_start=102
  _globals['_FXPRICESRESPONSE']._serialized_end=136
  _globals['_FXPRICESHANDLER']._serialized_start=138
  _globals['_FXPRICESHANDLER']._serialized_end=257
# @@protoc_insertion_point(module_scope)
