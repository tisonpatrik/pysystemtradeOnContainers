import asyncio

import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.utils.bounded_task_group import BoundedTaskGroup
from common.src.validation.instrument import Instrument
from raw_data.api.handlers.skew_handler import SkewHandler


class NegSkewOverInstrumentListHandler:
    def __init__(self, skew_handler: SkewHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.skew_handler = skew_handler
        self.max_concurrent_tasks = 8

    async def get_factor_values_over_instrument_list_async(self, instrument_list: list[Instrument], lookback: int) -> pd.DataFrame:
        self.logger.info("Fetching factor values for instruments")
        async with BoundedTaskGroup(max_parallelism=self.max_concurrent_tasks) as tg:
            # Schedule the tasks without awaiting, collecting coroutine objects instead
            tasks = [tg.create_task(self._get_skew_task(instrument, lookback)) for instrument in instrument_list]

        # Await all tasks to resolve the coroutines into DataFrames or Series
        all_factor_values = await asyncio.gather(*tasks)

        # Build DataFrame from the results
        instrument_symbols = [instrument.symbol for instrument in instrument_list]
        all_factor_values_df = pd.concat(all_factor_values, axis=1)
        all_factor_values_df.columns = instrument_symbols
        return all_factor_values_df

    def _get_skew_task(self, instrument: Instrument, lookback: int):
        """Return the appropriate skew or neg_skew coroutine based on the factor name."""
        return self.skew_handler.get_neg_skew_async(instrument.symbol, lookback=lookback)
