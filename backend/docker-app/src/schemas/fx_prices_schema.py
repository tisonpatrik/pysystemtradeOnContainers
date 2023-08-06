from uuid import UUID

from src.db.tables.fx_prices_table import FxPricesTableBase


class FxPricesCreate(FxPricesTableBase):
    ...


class FxPricesRead(FxPricesTableBase):
    id: UUID


class FxPricesPatch(FxPricesTableBase):
    ...
