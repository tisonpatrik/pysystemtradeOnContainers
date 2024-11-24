"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class RelativeSkewDeviationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SYMBOL_FIELD_NUMBER: builtins.int
    LOOKBACK_FIELD_NUMBER: builtins.int
    symbol: builtins.str
    lookback: builtins.int
    def __init__(
        self,
        *,
        symbol: builtins.str = ...,
        lookback: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["lookback", b"lookback", "symbol", b"symbol"]) -> None: ...

global___RelativeSkewDeviationRequest = RelativeSkewDeviationRequest

@typing.final
class RelativeSkewDeviationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SERIES_FIELD_NUMBER: builtins.int
    series: builtins.bytes
    def __init__(
        self,
        *,
        series: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["series", b"series"]) -> None: ...

global___RelativeSkewDeviationResponse = RelativeSkewDeviationResponse
