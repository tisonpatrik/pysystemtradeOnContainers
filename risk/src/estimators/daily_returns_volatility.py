from pandera.typing import Series

from common.src.validations.prices_schemas import DailyPrices
from common.src.validations.risk_schemas import DailyReturns, DailyReturnsVolatility
from risk.src.estimators.volatility import mixed_vol_calc


class DailyReturnsVolEstimator:

    def process_daily_returns_vol(
        self, daily_prices: Series[DailyPrices]
    ) -> Series[DailyReturnsVolatility]:
        price_returns = self.daily_returns(daily_prices)
        vol_multiplier = 1
        raw_vol = mixed_vol_calc(price_returns)

        vol = vol_multiplier * raw_vol
        return Series[DailyReturnsVolatility](vol)

    def daily_returns(self, daily_prices: Series[DailyPrices]) -> Series[DailyReturns]:
        """
        Gets daily returns (not % returns)
        """
        dailyreturns = daily_prices.diff()
        return Series[DailyReturns](dailyreturns)
