from uuid import UUID

from src.db.tables.transactions import TransactionBase


class TransactionCreate(TransactionBase):
    ...


class TransactionRead(TransactionBase):
    id: UUID


class TransactionPatch(TransactionBase):
    ...
