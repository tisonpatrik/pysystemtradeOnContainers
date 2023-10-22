"""
Module for mapping file tables and their corresponding directories.
"""
from typing import Dict
from pydantic import BaseModel, Field


class FileTableMapping(BaseModel):
    """
    Data model for storing table-to-directory mappings.
    """

    directory: str = Field(
        ..., description="The directory path where files are stored."
    )
    file_name: str = Field(..., description="The table name for data storage.")
    table: str = Field(..., description="The table name for data storage.")
    multiple_files: bool = Field(
        False, description="Whether multiple files need to be processed."
    )
    columns_mapping: Dict[str, str] = Field(
        ..., description="Column mapping from file to table."
    )
