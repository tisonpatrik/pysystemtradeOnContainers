import pandas as pd
from fastapi import Depends, HTTPException

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from common.src.logging.logger import AppLogger
from common.src.queries.db_queries.get_daily_prices import GetDailyPriceQuery
from common.src.utils.convertors import to_series
from common.src.validation.daily_prices import DailyPrices
from rules.workers.breakout.src.breakout import BreakoutService
from rules.workers.breakout.src.forecast_request import ForecastRequest


class BreakoutHandler:
    def __init__(
        self,
        repository: Repository = Depends(get_repository),
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.breaktout_service = BreakoutService()
        self.repository = repository

    async def get_breakout_async(self, request: ForecastRequest) -> pd.Series[float]:
        try:
            self.logger.info(
                f"Calculating breakout for symbol {request.symbol} with speed {request.speed}",
            )
            daily_prices = await self._get_daily_prices(request.symbol)
            breakout = self.breaktout_service.get_breakout(daily_prices, request.speed)
            return breakout
        except Exception as e:
            self.logger.error("Failed to compute breakout rule: %s", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    async def _get_daily_prices(self, symbol: str) -> pd.Series:
        statement = GetDailyPriceQuery(symbol=symbol)
        try:
            prices_data = await self.repository.fetch_many_async(statement)
            prices = to_series(
                prices_data,
                DailyPrices,
                DailyPrices.date_time,  # type: ignore[arg-type]
                DailyPrices.price,  # type: ignore[arg-type]
            )
            return prices
        except Exception as e:
            self.logger.error(
                f"Database error when fetching currency for symbol {symbol}: {e}",
            )
            raise
