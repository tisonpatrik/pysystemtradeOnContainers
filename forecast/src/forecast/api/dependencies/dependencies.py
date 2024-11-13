from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.dependencies.db_setup import setup_async_database
from forecast.api.handlers.combined_forecast_handler import CombineForecastHandler
from forecast.api.handlers.combined_forecast_without_multiplier_handler import CombinedForecastWithoutMultiplierHandler
from forecast.api.handlers.raw_combined_forecast_handler import RawCombineForecastHandler
from forecast.api.handlers.weighted_forecasts_without_multiplier_handler import WeightedForecastsWithoutMultiplierHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_database(app):
        yield


def get_weighted_forecasts_without_multiplier_handler() -> WeightedForecastsWithoutMultiplierHandler:
    return WeightedForecastsWithoutMultiplierHandler()


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
