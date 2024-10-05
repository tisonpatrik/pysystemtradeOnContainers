import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from common.src.repositories.raw_data_client import RawDataClient
from rules.src.services.carry import CarryService


class RelativeCarryHandler:
    def __init__(self, raw_data_client: RawDataClient, instrument_client: InstrumentsClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.raw_data_client = raw_data_client
        self.instrument_client = instrument_client
        self.carry_service = CarryService()

    async def get_relative_carry_async(self, symbol: str) -> pd.Series:
        try:
            self.logger.info("Calculating Carry rule for %s", symbol)
            asset_class = await self.instrument_client.get_asset_class_async(symbol=symbol)
            smoothed_carry = await self.raw_data_client.get_smoothed_carry_async(symbol)
            median_carry_for_asset_class = await self.raw_data_client.get_median_carry_for_asset_class_async(asset_class.asset_class)
            return self.carry_service.calculate_relative_carry(
                smoothed_carry=smoothed_carry, median_carry_for_asset_class=median_carry_for_asset_class
            )

        except Exception:
            self.logger.exception("Error calculating Carry rule for %s", symbol)
            raise
