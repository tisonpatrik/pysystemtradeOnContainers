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
class FxPricesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SYMBOL_FIELD_NUMBER: builtins.int
    BASE_CURRENCY_FIELD_NUMBER: builtins.int
    symbol: builtins.str
    base_currency: builtins.str
    def __init__(
        self,
        *,
        symbol: builtins.str = ...,
        base_currency: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["base_currency", b"base_currency", "symbol", b"symbol"]) -> None: ...

global___FxPricesRequest = FxPricesRequest

@typing.final
class FxPricesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SERIES_FIELD_NUMBER: builtins.int
    series: builtins.bytes
    def __init__(
        self,
        *,
        series: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["series", b"series"]) -> None: ...

global___FxPricesResponse = FxPricesResponse
