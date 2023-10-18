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


# Usage example:
mapping_data = [
    {
        "Directory": "/path/in/container/csvconfig",
        "Tables": [
            "instrument_config",
            "instrument_metadata",
            "roll_config",
            "spread_cost",
        ],
    },
    {
        "Directory": "/path/in/container/adjusted_prices_csv",
        "Tables": "adjusted_prices",
    },
    {"Directory": "/path/in/container/fx_prices_csv", "Tables": "fx_prices"},
    {
        "Directory": "/path/in/container/multiple_prices_csv",
        "Tables": "multiple_prices",
    },
    {"Directory": "/path/in/container/roll_calendars_csv", "Tables": "roll_calendars"},
]

validated_mapping = [FileTableMapping(**data) for data in mapping_data]
