from uuid import UUID

from src.db.tables.business_data_tables.roll_calendars_table import RollCalendarsTableBase


class RollCalendarsCreate(RollCalendarsTableBase):
    ...


class RollCalendarsRead(RollCalendarsTableBase):
    id: UUID


class RollCalendarsPatch(RollCalendarsTableBase):
    ...
