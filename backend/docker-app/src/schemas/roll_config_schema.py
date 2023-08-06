from uuid import UUID

from src.db.tables.roll_config_table import RollConfigTableBase


class RollConfigCreate(RollConfigTableBase):
    ...


class RollConfigRead(RollConfigTableBase):
    id: UUID


class RollConfigPatch(RollConfigTableBase):
    ...
