import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.risk_client import RiskClient
from rules.src.services.cross_sectional_mean_reversion import CSMeanReversionService


class CSMeanReversionHandler:
    def __init__(
        self,
        risk_client: RiskClient,
        instrument_repository: InstrumentsRepository,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.risk_client = risk_client
        self.instrument_repository = instrument_repository
        self.cs_mean_reversion_service = CSMeanReversionService()

    async def get_cs_mean_reversion_async(self, symbol: str, speed: int) -> pd.Series:
        try:
            self.logger.info("Calculating Momentum rule for %s with Lfast %d", symbol, speed)
            symbol_prices = await self.risk_client.get_normalized_price_for_instrument_async(symbol)
            asset_class = await self.instrument_repository.get_asset_class_async(symbol)
            asset_prices = await self.risk_client.get_normalized_prices_for_asset_class_async(symbol, asset_class.asset_class)
            print(symbol_prices)
            print(asset_prices)
            return self.cs_mean_reversion_service.calculate_cross_sectional_mean_reversion(
                normalised_price_this_instrument=symbol_prices, normalised_price_for_asset_class=asset_prices, horizon=speed
            )

        except Exception as e:
            self.logger.exception("Unexpected error calculating momentum for %s with Lfast %d", symbol, speed)
            raise ValueError(f"An error occurred while calculating momentum for {symbol} with Lfast {speed}.") from e
