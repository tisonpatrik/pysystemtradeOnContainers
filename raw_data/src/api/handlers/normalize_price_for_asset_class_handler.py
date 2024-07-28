import pandas as pd

from common.src.cqrs.api_queries.get_normalized_price_for_asset_class_query import NormalizedPriceForAssetClassQuery
from common.src.logging.logger import AppLogger
from common.src.repositories.instruments_repository import InstrumentsRepository
from common.src.repositories.risk_repository import RiskClient
from common.src.utils.volatility import daily_returns


class NormalizedPriceForAssetClassHandler:
    def __init__(self, instrument_repository: InstrumentsRepository, risk_client: RiskClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_repository = instrument_repository
        self.risk_client = risk_client

    async def get_normalized_price_for_asset_class_async(
        self, get_normalized_price_query: NormalizedPriceForAssetClassQuery
    ) -> pd.DataFrame:
        try:
            self.logger.info(f"Fetching normalized prices for asset class {get_normalized_price_query}")
            asset_class = await self.instrument_repository.get_asset_class_async(get_normalized_price_query.symbol)
            instruments = await self.instrument_repository.get_instruments_for_asset_class_async(asset_class.asset_class)
            print(instruments)
            return pd.DataFrame()
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching FX prices: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

    async def _daily_vol_normalised_price_for_list_of_instruments(self, list_of_instruments: list) -> pd.Series:
        norm_returns = await self._aggregate_daily_vol_normalised_returns_for_list_of_instruments(list_of_instruments)
        norm_price = norm_returns.cumsum()

        return norm_price

    async def _aggregate_daily_vol_normalised_returns_for_list_of_instruments(self, list_of_instruments: list) -> pd.Series:
        aggregate_returns_across_instruments_list = [
            await self.get_daily_vol_normalised_returns(instrument_code) for instrument_code in list_of_instruments
        ]

        aggregate_returns_across_instruments = pd.concat(aggregate_returns_across_instruments_list, axis=1)
        median_returns = aggregate_returns_across_instruments.median(axis=1)
        return median_returns

    async def get_daily_vol_normalised_returns(self, instrument_code: str) -> pd.Series:
        prices = pd.Series()
        returnvol_data = await self.risk_client.get_daily_retuns_vol_async(instrument_code)
        returnvol = returnvol_data.shift(1)
        dailyreturns = daily_returns(prices)
        norm_return = dailyreturns / returnvol

        return norm_return
