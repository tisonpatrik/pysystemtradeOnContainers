from uuid import UUID

from src.db.tables.config_tables.spread_costs_table import SpreadCostTableBase


class SpreadCostCreate(SpreadCostTableBase):
    ...


class SpreadCostRead(SpreadCostTableBase):
    id: UUID


class SpreadCostPatch(SpreadCostTableBase):
    ...
