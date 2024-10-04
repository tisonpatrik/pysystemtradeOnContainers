import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.prices_client import PricesClient
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.momentum import MomentumService


class MomentumHandler:
    def __init__(self, prices_repository: PricesClient, raw_data_client: RawDataClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.prices_repository = prices_repository
        self.raw_data_client = raw_data_client
        self.momentum_service = MomentumService()

    async def get_momentum_async(self, symbol: str, Lfast: int) -> pd.Series:
        try:
            self.logger.info("Calculating Momentum rule for %s with Lfast %d", symbol, Lfast)
            daily_prices = await self.prices_repository.get_daily_prices_async(symbol)
            daily_vol = await self.raw_data_client.get_daily_returns_vol_async(symbol)
            return self.momentum_service.calculate_ewmac(daily_prices, daily_vol, Lfast)

        except Exception as e:
            self.logger.exception("Unexpected error calculating momentum for %s with Lfast %d", symbol, Lfast)
            raise ValueError(f"An error occurred while calculating momentum for {symbol} with Lfast {Lfast}.") from e
