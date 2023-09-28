"""
Module for Managing Schemas.

This module consolidates the various schemas for configurations and raw data tables.
It offers utility functions to get these schemas either collectively or based on their 
type (config or raw data).

Note: This docstring provides specific details about the module's purpose and functionalities.
"""

from src.db.schemas.config_schemas.instrument_config_schema import (
    InstrumentConfigSchema,
)
from src.db.schemas.config_schemas.instrument_metadata_schema import (
    InstrumentMetadataSchema,
)
from src.db.schemas.config_schemas.roll_config_schema import RollConfigSchema
from src.db.schemas.config_schemas.spread_cost_schema import SpreadCostSchema
from src.db.schemas.raw_data_schemas.adjusted_prices_schema import AdjustedPricesSchema
from src.db.schemas.raw_data_schemas.fx_prices_schema import FxPricesSchema
from src.db.schemas.raw_data_schemas.multiple_prices_schema import MultiplePricesSchema
from src.db.schemas.raw_data_schemas.roll_calendars_schema import RollCalendarsSchema


def get_schemas():
    """
    Get all schemas.

    This function returns a list of instantiated schema objects for both configuration and raw data.

    Returns:
        list: A list of schema objects.
    """
    return [
        InstrumentConfigSchema(),
        #InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema(),
        AdjustedPricesSchema(),
        FxPricesSchema(),
        MultiplePricesSchema(),
        RollCalendarsSchema(),
    ]


def get_configs_schemas():
    """
    Get configuration schemas.

    This function returns a list of instantiated schema objects that are specifically for configurations.

    Returns:
        list: A list of schema objects related to configurations.
    """
    return [
        InstrumentConfigSchema(),
        #InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema(),
    ]


def get_raw_data_schemas():
    """
    Get raw data schemas.

    This function returns a list of instantiated schema objects that are specifically for raw data tables.

    Returns:
        list: A list of schema objects related to raw data tables.
    """
    return [
        AdjustedPricesSchema(),
        FxPricesSchema(),
        MultiplePricesSchema(),
        RollCalendarsSchema(),
    ]
