"""
This module defines a Pydantic BaseModel class, CsvOutput, for representing CSV output data.
"""
from typing import List, Dict
from pydantic import BaseModel


class CsvOutput(BaseModel):
    """
    CsvOutput Class

    This class defines a Pydantic BaseModel for representing CSV output data.

    Attributes:
        full_path (str): The full path to the CSV file.
        table (str): Table name correspond to db.
        data (List[Dict[str, str]]): The data stored in a list of dictionaries.

    """

    full_path: str
    table: str
    data: List[Dict[str, str]]
