from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from common.src.clients.rules_signals_client import RulesSignalsClient
from common.src.dependencies.core_dependencies import get_rules_signals_client
from common.src.dependencies.db_setup import setup_async_database
from common.src.dependencies.rest_client_setup import setup_async_client
from forecast.api.handlers.combined_forecast_handler import CombineForecastHandler
from forecast.api.handlers.combined_forecast_without_multiplier_handler import CombinedForecastWithoutMultiplierHandler
from forecast.api.handlers.expensive_trading_rules_post_processing_handler import ExpensiveTradingRulesPostProcessingHandler
from forecast.api.handlers.fixed_forecast_weights_as_dict_handler import FixedForecastWeightsAsDictHandler
from forecast.api.handlers.forecast_weights_handler import ForecastWeightsHandler
from forecast.api.handlers.forecasts_given_rule_list_handler import ForecastGivenRuleListHandler
from forecast.api.handlers.raw_combined_forecast_handler import RawCombineForecastHandler
from forecast.api.handlers.raw_fixed_forecast_weights_handlers import RawFixedForecastWeightsHandler
from forecast.api.handlers.raw_monthly_forecast_weights_handler import RawMonthlyForecastWeightsHandler
from forecast.api.handlers.unsmoothed_forecast_weights_handler import UnsmoothedForecastWeightsHandler
from forecast.api.handlers.weighted_forecasts_without_multiplier_handler import WeightedForecastsWithoutMultiplierHandler


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with setup_async_client(app), setup_async_database(app):
        yield


def get_forecasts_given_rule_list_handler(
    rules_signals_client: RulesSignalsClient = Depends(get_rules_signals_client),
) -> ForecastGivenRuleListHandler:
    return ForecastGivenRuleListHandler(rules_signals_client=rules_signals_client)


def get_expensive_trading_rules_post_processing_handler(
    rules_signals_client: RulesSignalsClient = Depends(get_rules_signals_client),
) -> ExpensiveTradingRulesPostProcessingHandler:
    return ExpensiveTradingRulesPostProcessingHandler(rules_signals_client=rules_signals_client)


def get_fixed_forecast_weights_as_dict_handler(
    expensive_trading_rules_post_processing_handler: ExpensiveTradingRulesPostProcessingHandler = Depends(
        get_expensive_trading_rules_post_processing_handler
    ),
) -> FixedForecastWeightsAsDictHandler:
    return FixedForecastWeightsAsDictHandler(
        expensive_trading_rules_post_processing_handler=expensive_trading_rules_post_processing_handler
    )


def get_raw_fixed_forecast_weights_handlers(
    fixed_forecast_weights_as_dict_handler: FixedForecastWeightsAsDictHandler = Depends(get_fixed_forecast_weights_as_dict_handler),
) -> RawFixedForecastWeightsHandler:
    return RawFixedForecastWeightsHandler(fixed_forecast_weights_as_dict_handler=fixed_forecast_weights_as_dict_handler)


def get_raw_monthly_forecast_weights_handler(
    raw_fixed_forecast_weights_handlers: RawFixedForecastWeightsHandler = Depends(get_raw_fixed_forecast_weights_handlers),
) -> RawMonthlyForecastWeightsHandler:
    return RawMonthlyForecastWeightsHandler(raw_fixed_forecast_weights_handlers=raw_fixed_forecast_weights_handlers)


def get_unsmoothed_forecast_weights_handler(
    raw_monthly_forecast_weights_handler: RawMonthlyForecastWeightsHandler = Depends(get_raw_monthly_forecast_weights_handler),
) -> UnsmoothedForecastWeightsHandler:
    return UnsmoothedForecastWeightsHandler(raw_monthly_forecast_weights_handler=raw_monthly_forecast_weights_handler)


def get_forecast_weights_handler(
    unsmoothed_forecast_weights_handler: UnsmoothedForecastWeightsHandler = Depends(get_unsmoothed_forecast_weights_handler),
) -> ForecastWeightsHandler:
    return ForecastWeightsHandler(unsmoothed_forecast_weights_handler=unsmoothed_forecast_weights_handler)


def get_weighted_forecasts_without_multiplier_handler(
    rules_signals_client: RulesSignalsClient = Depends(get_rules_signals_client),
    forecasts_given_rule_list_handler: ForecastGivenRuleListHandler = Depends(get_forecasts_given_rule_list_handler),
    forecast_weights_handler: ForecastWeightsHandler = Depends(get_forecast_weights_handler),
) -> WeightedForecastsWithoutMultiplierHandler:
    return WeightedForecastsWithoutMultiplierHandler(
        rules_signals_client=rules_signals_client,
        forecasts_given_rule_list_handler=forecasts_given_rule_list_handler,
        forecast_weights_handler=forecast_weights_handler,
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
