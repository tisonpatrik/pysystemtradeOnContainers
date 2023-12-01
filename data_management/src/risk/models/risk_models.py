from sqlalchemy import Column, Float, ForeignKey, Integer, PrimaryKeyConstraint, String
from src.core.models.base_model import BaseModel


class DailyReturnsVolatility(BaseModel):
    """
    ORM class for the 'daily_returns_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "daily_returns_volatility"

    unix_date_time = Column(Integer)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    daily_returns_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<DailyReturnsVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.daily_returns_volatility})>"


class InstrumentVolatility(BaseModel):
    """
    ORM class for the 'instrument_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "instrument_volatility"
    unix_date_time = Column(Integer)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    instrument_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<InstrumentVolatility(unix_date_time={self.unix_date_time}, symbol={self.symbol}, volatility={self.instrument_volatility})>"


class CumulativeDailyVolNormalizedReturns(BaseModel):
    """
    ORM class for the 'cumulative_daily_vol_normalized_returns' table.
    Represents cumulative normalized volatility metrics for financial instruments.
    """

    __tablename__ = "cumulative_daily_vol_normalized_returns"
    unix_date_time = Column(Integer)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    normalized_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<CumulativeDailyVolNormalizedReturns(unix_date_time={self.unix_date_time}, symbol={self.symbol}, normalized_volatility={self.normalized_volatility})>"


class NormalisedPriceForAssetClass(BaseModel):
    """
    ORM class for the 'normalised_price_for_asset_class' table.
    Represents cumulative normalized volatility metrics for financial instruments.
    """

    __tablename__ = "normalised_price_for_asset_class"

    unix_date_time = Column(Integer)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    normalized_price = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(unix_date_time, symbol),)

    def __repr__(self):
        return f"<NormalisedPriceForAssetClass(unix_date_time={self.unix_date_time}, symbol={self.symbol}, normalized_price={self.normalized_price})>"
