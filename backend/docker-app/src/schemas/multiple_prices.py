from uuid import UUID

from src.db.tables.transactions import TransactionBase


class MultiplePricesCreate(TransactionBase):
    ...


class MultiplePricesRead(TransactionBase):
    id: UUID


class MultiplePricesPatch(TransactionBase):
    ...
