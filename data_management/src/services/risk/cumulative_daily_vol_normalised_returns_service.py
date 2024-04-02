from src.estimators.comulative_vol_normalised_returns import (
    CumulativeVolNormalisedReturns,
)
# from src.services.risk.daily_volatility_normalised_returns_service import (
#     DailyVolatilityNormalisedReturnsService,
# )

from common.src.logging.logger import AppLogger


class CumulativeDailyVolatilityNormalisedReturnsService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.comulative_vol_normalised_returns = CumulativeVolNormalisedReturns()
        # self.daily_vol_normalised_returns_service = (
        #     DailyVolatilityNormalisedReturnsService(db_session)
        # )

    async def get_cumulative_vol_for_prices_async(self, symbol: str):
        """
        Asynchronously fetches cumulative returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            # normalised_returns = await self.daily_vol_normalised_returns_service.get_daily_vol_normalised_returns_async(
            #     symbol
            # )

            # cumulative_normalised_returns = self.comulative_vol_normalised_returns.get_cumulative_daily_vol_normalised_returns(
            #     normalised_returns
            # )
            # return cumulative_normalised_returns
            print("neco")

        except Exception as exc:
            error_message = f"Failed to get cumulative returns volatility asynchronously for symbol '{symbol}': {exc}"
            self.logger.error(error_message, exc_info=True)
            raise ValueError(error_message)
