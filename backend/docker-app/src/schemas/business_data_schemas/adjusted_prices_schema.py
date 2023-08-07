from uuid import UUID

from src.db.tables.business_data_tables.adjusted_prices_table import AdjustedPricesTableBase


class AdjustedPricesCreate(AdjustedPricesTableBase):
    ...


class AdjustedPricesRead(AdjustedPricesTableBase):
    id: UUID


class AdjustedPricesPatch(AdjustedPricesTableBase):
    ...
