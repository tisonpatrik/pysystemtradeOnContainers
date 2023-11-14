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

    Attributes:
        unix_date_time (int): UNIX timestamp, part of the primary key.
        symbol (str): Stock symbol, part of the primary key.
        price (float): Adjusted price of the stock.
    """

    __tablename__ = "adjusted_prices"
    directory = "/path/in/container/adjusted_prices_csv"
    # Defining the table schema
    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    price = Column(Float)


class FxPrices(BaseModel):
    """
    ORM class for the 'fx_prices' table. Represents foreign exchange prices.

    Attributes:
        unix_date_time (int): UNIX timestamp, part of the primary key.
        symbol (str): Currency pair symbol, part of the primary key.
        price (float): Price of the currency pair.
    """

    __tablename__ = "/path/in/container/fx_prices_csv"
    file_name = "adjusted_prices.csv"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    price = Column(Float)


class MultiplePrices(BaseModel):
    """
    ORM class for the 'multiple_prices' table. Represents various price-related metrics.

    Attributes:
        unix_date_time (int): UNIX timestamp, part of the primary key.
        symbol (str): Financial instrument symbol, part of the primary key.
        carry (float): Carry value.
        carry_contract (int): Contract number for carry.
        price (float): Price of the instrument.
        price_contract (int): Contract number for price.
        forward (float): Forward price.
        forward_contract (int): Contract number for forward.
    """

    __tablename__ = "/path/in/container/multiple_prices_csv"

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

    Attributes:
        unix_date_time (int): UNIX timestamp, part of the primary key.
        symbol (str): Symbol of the futures contract, part of the primary key.
        current_contract (int): The current contract identifier.
        next_contract (int): The next contract identifier.
        carry_contract (int): Identifier for the carry contract.
    """

    __tablename__ = "/path/in/container/roll_calendars_csv"

    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    current_contract = Column(Integer)
    next_contract = Column(Integer)
    carry_contract = Column(Integer)

