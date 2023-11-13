from sqlalchemy import Column, Integer, String, Float
from src.core.models.base_model import Base


class RobustVolatility(Base):
    """
    ORM class for the 'robust_volatility' table. Represents volatility metrics for financial instruments.

    Attributes:
        unix_date_time (int): UNIX timestamp, part of the primary key.
        symbol (str): Financial instrument symbol, part of the primary key.
        volatility (float): Volatility measure of the instrument.
    """

    __tablename__ = "robust_volatility"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    volatility = Column(Float)

    def __repr__(self):
        return f"<RobustVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"


class InstrumentVolatility(Base):
    """
    ORM class for the 'instrument_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "instrument_volatility"
    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    volatility = Column(Float)

    def __repr__(self):
        return f"<InstrumentVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"
