"""
Module: DataFrameContainer
Purpose: This module defines the DataFrameContainer class which encapsulates a Pandas DataFrame along with its corresponding table name. 
It provides methods for interacting with these encapsulated attributes.
"""
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DataFrameContainer:
    """
    Encapsulates a Pandas DataFrame along with its corresponding table name.
    """

    data_frame: pd.DataFrame
    table_name: str
