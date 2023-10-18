"""
This module defines the AdjustedPricesSchema class, 
which models the structure of the 'adjusted_prices' table in the database.
"""

from pydantic import BaseModel


class AdjustedPricesSchema(BaseModel):
    """
    Defines the schema for the Adjusted Prices table in the database.
    Fields:
        - unix_date_time: The timestamp in UNIX format.
        - symbol: The trading symbol of the instrument.
        - price: The adjusted price of the instrument.
    """

    unix_date_time: int
    symbol: str
    price: float
