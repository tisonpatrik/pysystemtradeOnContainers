"""
This module defines an ORM class for interacting with the 'adjusted_prices' table in the database.
It maps the database table to a Python object for easier manipulation and querying of data.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AdjustedPrices(Base):
    """
    ORM class for the 'adjusted_prices' table in the database.

    Attributes:
        unix_date_time (int): The primary key column representing the UNIX timestamp of the price.
        symbol (str): Another part of the composite primary key, representing the stock symbol.
        price (float): The adjusted price of the stock.

    Each instance of this class represents a row in the 'adjusted_prices' table.
    """

    __tablename__ = "adjusted_prices"

    # Defining the table schema
    unix_date_time = Column(Integer, primary_key=True)
    symbol = Column(String(50), primary_key=True)
    price = Column(Float)

    def __repr__(self):
        return f"<AdjustedPrices(unix_date_time={self.unix_date_time}, symbol={self.symbol}, price={self.price})>"
