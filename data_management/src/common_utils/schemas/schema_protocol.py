from typing import Protocol, runtime_checkable
from sqlalchemy import Column


@runtime_checkable
class SchemaProtocol(Protocol):
    unix_date_time: Column
    symbol: Column
