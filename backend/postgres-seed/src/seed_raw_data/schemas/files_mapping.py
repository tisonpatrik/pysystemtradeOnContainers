"""
This module defines a Pydantic model for mapping directories to tables.
The FileTableMapping model ensures consistent structure for directory-to-table mappings.
"""
from typing import List, Union
from pydantic import BaseModel, Field


class FileTableMapping(BaseModel):
    """
    Defines a Pydantic model for mapping directories to corresponding tables.
    Fields:
        - directory: The directory where the CSV files are located.
        - tables: The tables that correspond to the given directory.
    """

    directory: str = Field(..., alias="Directory")
    tables: Union[str, List[str]] = Field(..., alias="Tables")
