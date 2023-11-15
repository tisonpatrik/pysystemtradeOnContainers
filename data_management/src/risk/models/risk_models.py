from sqlalchemy import Column, Integer, String, Float
from src.core.models.base_model import BaseModel

class RobustVolatility(BaseModel):
    """
    ORM class for the 'robust_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "robust_volatility"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    volatility = Column(Float)

    def __repr__(self):
        return f"<RobustVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"


class InstrumentVolatility(BaseModel):
    """
    ORM class for the 'instrument_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "instrument_volatility"
    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    volatility = Column(Float)

    def __repr__(self):
        return f"<InstrumentVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.volatility})>"
