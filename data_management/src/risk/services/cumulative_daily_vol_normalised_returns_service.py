from src.core.utils.logging import AppLogger
from src.risk.errors.cumulative_volatility_returns_errors import (
    CumulativeVolatilityReturnsCalculationError,
)
from src.risk.estimators.comulative_vol_normalised_returns import (
    CumulativeVolNormalisedReturns,
)
from src.risk.services.daily_volatility_normalised_returns_service import (
    DailyVolatilityNormalisedReturnsService,
)


class CumulativeDailyVolatilityNormalisedReturnsService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.comulative_vol_normalised_returns = CumulativeVolNormalisedReturns()
        self.daily_vol_normalised_returns_service = (
            DailyVolatilityNormalisedReturnsService(db_session)
        )

    async def get_cumulative_vol_for_prices_async(self, symbol: str):
        """
        Asynchronously fetches cumulative returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            normalised_returns = await self.daily_vol_normalised_returns_service.get_daily_vol_normalised_returns_async(
                symbol
            )

            cumulative_normalised_returns = self.comulative_vol_normalised_returns.get_cumulative_daily_vol_normalised_returns(
                normalised_returns
            )
            return cumulative_normalised_returns
        except Exception as exc:
            self.logger.error(
                "Failed to get daily returns volatility asynchronously: %s",
                exc,
                exc_info=True,
            )
            raise CumulativeVolatilityReturnsCalculationError(symbol, exc)
