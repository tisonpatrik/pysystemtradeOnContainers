from sqlalchemy import Column, Float, ForeignKey, Integer, PrimaryKeyConstraint, String
from src.core.models.base_model import BaseModel


class DailyReturnsVolatility(BaseModel):
    """
    ORM class for the 'daily_returns_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "daily_returns_volatility"

    unix_date_time = Column(Integer)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<DailyReturnsVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"


class InstrumentVolatility(BaseModel):
    """
    ORM class for the 'instrument_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "instrument_volatility"
    unix_date_time = Column(Integer)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<InstrumentVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"
