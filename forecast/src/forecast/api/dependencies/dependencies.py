from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.dependencies.core_dependencies import get_rules_signals_client
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.rest_client_setup import setup_async_client
from forecast.api.handlers.combined_forecast_handler import CombineForecastHandler
from forecast.api.handlers.combined_forecast_without_multiplier_handler import CombinedForecastWithoutMultiplierHandler
from forecast.api.handlers.forecasts_given_rule_list_handler import ForecastGivenRuleListHandler
from forecast.api.handlers.raw_combined_forecast_handler import RawCombineForecastHandler
from forecast.api.handlers.weighted_forecasts_without_multiplier_handler import WeightedForecastsWithoutMultiplierHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app):
        yield


def get_forecasts_given_rule_list_handler(
    rules_signals_client: RulesSignalsClient = Depends(get_rules_signals_client),
) -> ForecastGivenRuleListHandler:
    return ForecastGivenRuleListHandler(rules_signals_client=rules_signals_client)


def get_weighted_forecasts_without_multiplier_handler(
    rules_signals_client: RulesSignalsClient = Depends(get_rules_signals_client),
    forecasts_given_rule_list_handler: ForecastGivenRuleListHandler = Depends(get_forecasts_given_rule_list_handler),
) -> WeightedForecastsWithoutMultiplierHandler:
    return WeightedForecastsWithoutMultiplierHandler(
        rules_signals_client=rules_signals_client, forecasts_given_rule_list_handler=forecasts_given_rule_list_handler
    )


def get_combined_forecast_without_multiplier_handler(
    weighted_forecasts_without_multiplier_handler: WeightedForecastsWithoutMultiplierHandler = Depends(
        get_weighted_forecasts_without_multiplier_handler
    ),
) -> CombinedForecastWithoutMultiplierHandler:
    return CombinedForecastWithoutMultiplierHandler(
        weighted_forecasts_without_multiplier_handler=weighted_forecasts_without_multiplier_handler
    )


def get_raw_combined_forecast_handler(
    combined_forecast_without_multiplier_handler: CombinedForecastWithoutMultiplierHandler = Depends(
        get_combined_forecast_without_multiplier_handler
    ),
) -> RawCombineForecastHandler:
    return RawCombineForecastHandler(combined_forecast_without_multiplier_handler=combined_forecast_without_multiplier_handler)


async def get_combined_forecast_handler(
    raw_combined_forecast_handler: RawCombineForecastHandler = Depends(get_raw_combined_forecast_handler),
) -> CombineForecastHandler:
    return CombineForecastHandler(raw_combined_forecast_handler=raw_combined_forecast_handler)
