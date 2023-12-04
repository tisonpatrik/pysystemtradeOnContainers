from src.core.utils.logging import AppLogger
from src.risk.errors.cumulative_volatility_returns_errors import (
    CumulativeVolatilityReturnsCalculationError,
)
from src.risk.estimators.comulative_vol_normalised_returns import (
    CumulativeVolNormalisedReturns,
)


class CumulativeDailyVolatilityNormalisedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.comulative_vol_normalised_returns = CumulativeVolNormalisedReturns()

    async def get_cumulative_vol_for_prices_async(self, symbol, norm_return):
        """
        Asynchronously fetches cumulative returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            cumulative_returns = self.comulative_vol_normalised_returns.get_cumulative_daily_vol_normalised_returns(
                norm_return
            )
            return cumulative_returns
        except Exception as exc:
            self.logger.error(
                "Failed to get daily returns volatility asynchronously: %s",
                exc,
                exc_info=True,
            )
            raise CumulativeVolatilityReturnsCalculationError(symbol, exc)
