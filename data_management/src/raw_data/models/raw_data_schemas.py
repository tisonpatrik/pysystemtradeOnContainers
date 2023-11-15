"""
This module defines SQLAlchemy ORM classes for various financial tables, 
including adjusted prices, FX prices, multiple prices, and roll calendars. 
These classes facilitate database interactions in a Pythonic way.
"""

from sqlalchemy import Column, Integer, String, Float
from src.core.models.base_model import BaseModel

class AdjustedPrices(BaseModel):
    """
    ORM class for the 'adjusted_prices' table. Represents prices adjusted for factors
    like splits and dividends.
    """

    __tablename__ = "adjusted_prices"
    directory = "/path/in/container/adjusted_prices_csv"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    price = Column(Float)


class FxPrices(BaseModel):
    """
    ORM class for the 'fx_prices' table. Represents foreign exchange prices.
    """

    __tablename__ = "fx_prices"
    directory = "/path/in/container/fx_prices_csv"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    price = Column(Float)


class MultiplePrices(BaseModel):
    """
    ORM class for the 'multiple_prices' table. Represents various price-related metrics.
    """

    __tablename__ = "multiple_prices"
    directory = "/path/in/container/multiple_prices_csv"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    carry = Column(Float)
    carry_contract = Column(Integer)
    price = Column(Float)
    price_contract = Column(Integer)
    forward = Column(Float)
    forward_contract = Column(Integer)


class RollCalendars(BaseModel):
    """
    ORM class for the 'roll_calendars' table. Represents rolling calendar data for futures contracts.
    """

    __tablename__ = "roll_calendars"
    directory = "/path/in/container/roll_calendars_csv"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    current_contract = Column(Integer)
    next_contract = Column(Integer)
    carry_contract = Column(Integer)

