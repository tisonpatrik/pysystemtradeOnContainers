"""
Module: DataFrameContainer
Purpose: This module defines the DataFrameContainer class which encapsulates a Pandas DataFrame along with its corresponding table name. 
It provides methods for interacting with these encapsulated attributes.
"""
import pandas as pd


class DataFrameContainer:
    """
    Encapsulates a Pandas DataFrame along with its corresponding table name.
    """

    def __init__(self, data_frame: pd.DataFrame, table_name: str):
        """
        Initialize the DataFrameContainer with a DataFrame and a table name.
        """
        self.data_frame = data_frame
        self.table_name = table_name

    def get_data_frame(self) -> pd.DataFrame:
        """
        Retrieve the stored DataFrame.
        """
        return self.data_frame

    def get_table_name(self) -> str:
        """
        Retrieve the stored table name.
        """
        return self.table_name
