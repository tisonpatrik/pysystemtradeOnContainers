import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_client import InstrumentsClient
from risk.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler


class AggregatedReturnsForAssetClassHandler:
    def __init__(
        self,
        instrument_repository: InstrumentsClient,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler

    async def get_aggregated_returns_for_asset_async(self, asset_class: str) -> pd.Series:
        try:
            instruments = await self._get_instruments_for_asset_class(asset_class)
            aggregate_returns = await self._fetch_returns_for_instruments(instruments)
            return self._calculate_median_returns(aggregate_returns)

        except Exception:
            self.logger.exception("Error aggregating returns for asset class: %s", asset_class)
            raise

    async def _get_instruments_for_asset_class(self, asset_class: str) -> list:
        instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class)
        if not instruments:
            self.logger.warning("No instruments found for asset class: %s", asset_class)
            raise ValueError(f"No instruments found for asset class: {asset_class}")
        return instruments

    async def _fetch_returns_for_instruments(self, instruments: list) -> list:
        aggregate_returns = []
        for instrument in instruments:
            try:
                self.logger.info("Fetching returns for instrument: %s", instrument.symbol)
                returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalized_returns_async(instrument.symbol)
                if returns is not None:
                    aggregate_returns.append(returns)
            except Exception:
                self.logger.exception("Error fetching returns for instrument: %s", instrument.symbol)
        if not aggregate_returns:
            raise ValueError("No returns data found for instruments")
        return aggregate_returns

    def _calculate_median_returns(self, aggregate_returns: list) -> pd.Series:
        aggregated_data = pd.concat(aggregate_returns, axis=1)
        return aggregated_data.median(axis=1)
