from sqlalchemy import (
    BigInteger,
    Column,
    Float,
    ForeignKey,
    PrimaryKeyConstraint,
    String,
)
from src.core.models.base_model import BaseModel


class RobustVolatility(BaseModel):
    """
    ORM class for the 'robust_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "robust_volatility"

    unix_date_time = Column(BigInteger)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<RobustVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"


class InstrumentVolatility(BaseModel):
    """
    ORM class for the 'instrument_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "instrument_volatility"
    unix_date_time = Column(BigInteger)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<InstrumentVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"
