import asyncio

import pandas as pd

from common.logging.logger import AppLogger
from common.utils.bounded_task_group import BoundedTaskGroup
from common.validation.instrument import Instrument
from raw_data.api.handlers.skew_handler import SkewHandler


class NegSkewOverInstrumentListHandler:
    def __init__(self, skew_handler: SkewHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.skew_handler = skew_handler
        self.max_concurrent_tasks = 8

    async def get_negskew_over_instrument_list_async(self, instrument_list: list[Instrument], lookback: int) -> pd.DataFrame:
        self.logger.info("Fetching factor values for instruments")
        async with BoundedTaskGroup(max_parallelism=self.max_concurrent_tasks) as tg:
            tasks = [tg.create_task(self._get_skew_task(instrument, lookback)) for instrument in instrument_list]

        all_factor_values = await asyncio.gather(*tasks)

        instrument_symbols = [instrument.symbol for instrument in instrument_list]
        all_factor_values_df = pd.concat(all_factor_values, axis=1)
        all_factor_values_df.columns = pd.Index(instrument_symbols)
        return all_factor_values_df

    def _get_skew_task(self, instrument: Instrument, lookback: int):
        """Return the appropriate skew or neg_skew coroutine based on the factor name."""
        return self.skew_handler.get_neg_skew_async(instrument.symbol, lookback=lookback)
