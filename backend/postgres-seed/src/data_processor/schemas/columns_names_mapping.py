"""
This module defines the FileTableMapping class for managing table-to-column mappings.
"""

from typing import Dict
from pydantic import BaseModel


class FileTableMapping(BaseModel):
    """
    Represents a mapping between a table name and its column mappings.
    """

    table_name: str
    column_mapping: Dict[str, str]
