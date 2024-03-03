from sqlalchemy import Column, DateTime, Float, ForeignKey, PrimaryKeyConstraint, String

from common.database.base_model import BaseModel


class DailyReturnsVolatility(BaseModel):
    """
    ORM class for the 'daily_returns_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "daily_returns_volatility"

    date_time = Column(DateTime)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    daily_returns_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(date_time, symbol),)

    def __repr__(self):
        return f"<DailyReturnsVolatility(unix_date_time={self.date_time}, symbol={self.symbol}, volatility={self.daily_returns_volatility})>"


class InstrumentVolatility(BaseModel):
    """
    ORM class for the 'instrument_volatility' table. Represents volatility metrics for financial instruments.
    """

    __tablename__ = "instrument_volatility"
    date_time = Column(DateTime)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    instrument_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(date_time, symbol),)

    def __repr__(self):
        return f"<InstrumentVolatility(unix_date_time={self.date_time}, symbol={self.symbol}, volatility={self.instrument_volatility})>"


class DailyVolNormalizedReturns(BaseModel):
    """
    ORM class for the 'daily_vol_normalized_returns' table.
    Represents cumulative normalized volatility metrics for financial instruments.
    """

    __tablename__ = "daily_vol_normalized_returns"
    date_time = Column(DateTime)
    symbol = Column(String(50), ForeignKey("instrument_config.symbol"))
    normalized_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(date_time, symbol),)

    def __repr__(self):
        return f"<DailyVolNormalizedReturns(unix_date_time={self.date_time}, symbol={self.symbol}, normalized_volatility={self.normalized_volatility})>"


class DailyVolNormalisedPriceForAssetClass(BaseModel):
    """
    ORM class for the 'daily_vol_normalized_price_for_asset_class' table.
    Represents daily normalised price for asset class metrics for financial instruments.
    """

    __tablename__ = "daily_vol_normalised_price_for_asset_class"
    date_time = Column(DateTime)
    asset_class = Column(String(50))
    normalized_volatility = Column(Float)

    __table_args__ = (PrimaryKeyConstraint(date_time, asset_class),)

    def __repr__(self):
        return f"<DailyVolNormalisedPriceForAssetClass(unix_date_time={self.date_time}, asset_class={self.asset_class}, normalized_volatility={self.normalized_volatility})>"
