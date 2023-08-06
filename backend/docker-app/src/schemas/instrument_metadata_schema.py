from uuid import UUID

from src.db.tables.instrument_metadata_table import InstrumentMetadataTableBase


class InstrumentMetadataCreate(InstrumentMetadataTableBase):
    ...


class InstrumentMetadataRead(InstrumentMetadataTableBase):
    id: UUID


class InstrumentMetadataPatch(InstrumentMetadataTableBase):
    ...
