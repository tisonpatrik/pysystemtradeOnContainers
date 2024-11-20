import pandas as pd

from common.src.clients.forecast_client import ForecastClient
from common.src.cqrs.api_queries.positions_queries.get_subsystem_positions import GetSubsystemPositionForInstrument
from common.src.logging.logger import AppLogger
from positions.api.handlers.average_position_at_subsystem_level_handler import AveragePositionAtSubsystemLevelHandler


class PositionsHandler:
    def __init__(
        self,
        forecast_client: ForecastClient,
        average_position_at_subsystem_level_handler: AveragePositionAtSubsystemLevelHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.forecast_client = forecast_client
        self.average_position_at_subsystem_level_handler = average_position_at_subsystem_level_handler

    async def get_subsystem_position_async(self, request: GetSubsystemPositionForInstrument) -> pd.Series:
        self.logger.info("Starting to get average position at subsystem level.")
        vol_scalar = await self.average_position_at_subsystem_level_handler.get_average_position_at_subsystem_level_async(
            request.symbol, request.base_currency, request.notional_trading_capital, request.percentage_volatility_target
        )
        forecast = await self.forecast_client.get_combinated_forecast(request.symbol)
        vol_scalar = vol_scalar.reindex(forecast.index, method="ffill")
        if vol_scalar.isnull():
            pass
        return vol_scalar
