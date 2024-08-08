import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from raw_data.src.api.handlers.daily_vol_normalized_returns_handler import DailyvolNormalizedReturnsHandler


class AggregatedReturnsForAssetClassHandler:
    def __init__(self,
        instrument_repository: InstrumentsRepository,
        daily_vol_normalized_returns_handler: DailyvolNormalizedReturnsHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.daily_vol_normalized_returns_handler = daily_vol_normalized_returns_handler


    async def get_aggregated_returns_for_asset_class_async(self, asset_class: str) -> pd.DataFrame:
            try:
                self.logger.info(f"Fetching instruments for asset class: {asset_class}")
                instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class)

                if not instruments:
                    self.logger.warning(f"No instruments found for asset class: {asset_class}")
                    raise ValueError(f"No instruments found for asset class: {asset_class}")

                aggregate_returns_across_instruments_list = []

                for instrument_code in instruments:
                    try:
                        self.logger.info(f"Fetching returns for instrument: {instrument_code.symbol}")
                        returns = await self.daily_vol_normalized_returns_handler.get_daily_vol_normalised_returns(instrument_code.symbol)
                        aggregate_returns_across_instruments_list.append(returns)
                    except Exception as e:
                        self.logger.error(f"Error fetching returns for instrument {instrument_code.symbol}: {e}")

                if not aggregate_returns_across_instruments_list:
                    self.logger.warning(f"No returns data found for asset class: {asset_class}")
                    raise ValueError(f"No returns data found for asset class: {asset_class}")

                aggregate_returns_across_instruments = pd.concat(aggregate_returns_across_instruments_list, axis=1)
                self.logger.info(f"Successfully aggregated returns for asset class: {asset_class}")
                return aggregate_returns_across_instruments

            except Exception as e:
                self.logger.error(f"Error in get_aggregated_returns_across_instruments for asset class {asset_class}: {e}")
                raise ValueError(f"Error processing returns for asset class {asset_class}: {e}")
