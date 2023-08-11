from sqlmodel import Field, SQLModel

from src.db.tables.base_class import TimestampModel, UUIDModel

class TransactionBase(SQLModel):
    amount: int = Field(nullable=False)
    description: str = Field(nullable=False)


class Transaction(TransactionBase, UUIDModel, TimestampModel, table=True):
    __tablename__ = "transactions"
