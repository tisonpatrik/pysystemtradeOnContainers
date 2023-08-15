from uuid import UUID

from src.db.tables.transactions_tables import TransactionBase


class TransactionCreate(TransactionBase):
    ...


class TransactionRead(TransactionBase):
    id: UUID


class TransactionPatch(TransactionBase):
    ...
