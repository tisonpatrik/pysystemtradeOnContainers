from uuid import UUID

from src.db.tables.instrument_config_table import InstrumentConfigTableBase


class InstrumentConfigCreate(InstrumentConfigTableBase):
    ...


class InstrumentConfigRead(InstrumentConfigTableBase):
    id: UUID


class InstrumentConfigPatch(InstrumentConfigTableBase):
    ...
