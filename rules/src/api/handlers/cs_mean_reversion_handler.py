import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.cross_sectional_mean_reversion import CSMeanReversionService


class CSMeanReversionHandler:
    def __init__(
        self,
        raw_data_client: RawDataClient,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.cs_mean_reversion_service = CSMeanReversionService()

    async def get_cs_mean_reversion_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info("Calculating Cross sectional mean reversion rule for %s with speed %d", symbol, speed)
            symbol_prices = await self.raw_data_client.get_cumulative_daily_vol_normalised_returns_async(symbol)
            asset_prices = await self.raw_data_client.get_normalized_prices_for_asset_class_async(symbol)
            return self.cs_mean_reversion_service.calculate_cross_sectional_mean_reversion(
                normalized_price_this_instrument=symbol_prices, normalized_price_for_asset_class=asset_prices, horizon=speed
            )

        except Exception as e:
            self.logger.exception("Unexpected error calculating momentum for %s with Lfast %d", symbol, speed)
            raise ValueError(f"An error occurred while calculating momentum for {symbol} with Lfast {speed}.") from e
