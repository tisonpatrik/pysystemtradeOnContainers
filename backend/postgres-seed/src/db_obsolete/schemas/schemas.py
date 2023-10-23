"""
This module serves as an aggregator for different schema objects used to configure database tables.
"""

from src.db_obsolete.schemas.config_schemas.instrument_config_schema import (
    InstrumentConfigSchema,
)
from src.db_obsolete.schemas.config_schemas.roll_config_schema import RollConfigSchema
from src.db_obsolete.schemas.config_schemas.spread_cost_schema import SpreadCostSchema
from src.db_obsolete.schemas.raw_data_schemas.adjusted_prices_schema import (
    AdjustedPricesSchema,
)
from src.db_obsolete.schemas.raw_data_schemas.fx_prices_schema import FxPricesSchema
from src.db_obsolete.schemas.raw_data_schemas.multiple_prices_schema import (
    MultiplePricesSchema,
)
from src.db_obsolete.schemas.raw_data_schemas.roll_calendars_schema import (
    RollCalendarsSchema,
)
from src.db_obsolete.schemas.risk_schemas.robust_volatility import RobustVolatility


def get_schemas():
    """
    Aggregates and returns all schema objects.

    Returns:
        list: A list containing all schema objects.
    """
    return get_configs_schemas() + get_raw_data_schemas() + get_risk_schemas()


def get_data_schemas():
    """
    Aggregates and returns all data schema objects.

    Returns:
        list: A list containing all data schema objects.
    """
    return get_configs_schemas() + get_raw_data_schemas()


def get_configs_schemas():
    """
    Returns a list of schema objects related to configurations.

    Returns:
        list: A list containing schema objects related to configurations.
    """
    return [
        InstrumentConfigSchema(),
        # InstrumentMetadataSchema(),
        RollConfigSchema(),
        SpreadCostSchema(),
    ]


def get_raw_data_schemas():
    """
    Returns a list of schema objects related to raw data.

    Returns:
        list: A list containing schema objects related to raw data.
    """
    return [
        AdjustedPricesSchema(),
        FxPricesSchema(),
        MultiplePricesSchema(),
        RollCalendarsSchema(),
    ]


def get_risk_schemas():
    return [
        RobustVolatility(),
    ]