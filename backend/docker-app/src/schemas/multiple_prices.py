from uuid import UUID

from src.db.tables.multiple_prices import MultiplePricesBase


class MultiplePricesCreate(MultiplePricesBase):
    ...


class MultiplePricesRead(MultiplePricesBase):
    id: UUID


class MultiplePricesPatch(MultiplePricesBase):
    ...
