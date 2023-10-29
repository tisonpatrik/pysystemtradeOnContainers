"""
This module defines the RobustVolatilitySchema class, 
which models the structure of the 'robust_volatility' table in the database.
"""
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True, order=True)
class RobustVolatilitySchema:
    """
    Defines the schema for the Robust Volatility table in the database.
    """

    index_column: str = field(default="unix_date_time")
    columns: Dict[str, str] = field(default_factory=lambda: {"price": "volatility"})
