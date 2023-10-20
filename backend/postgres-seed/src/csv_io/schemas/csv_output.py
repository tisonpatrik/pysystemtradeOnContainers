"""
Module: csv_output_module

This module defines a Pydantic BaseModel for representing CSV output data.

"""

from pandas import DataFrame
from pydantic import BaseModel


class CsvOutput(BaseModel):
    """
    CsvOutput Class

    This class defines a Pydantic BaseModel for representing CSV output data.

    Attributes:
        full_path (str): The full path to the CSV file.
        dataframe (DataFrame): The data stored in a Pandas DataFrame.

    """

    full_path: str
    dataframe: DataFrame
