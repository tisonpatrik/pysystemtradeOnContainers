from uuid import UUID

from src.db.tables.multiple_prices_table import MultiplePricesTableBase


class MultiplePricesCreate(MultiplePricesTableBase):
    ...


class MultiplePricesRead(MultiplePricesTableBase):
    id: UUID


class MultiplePricesPatch(MultiplePricesTableBase):
    ...
