import asyncio

import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.validation.instrument import Instrument
from raw_data.src.api.handlers.skew_handler import SkewHandler


class FactorValuesOverInstrumentListHandler:
    def __init__(self, skew_handler: SkewHandler, max_concurrent_tasks: int = 5):
        self.logger = AppLogger.get_instance().get_logger()
        self.skew_handler = skew_handler
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def fetch_with_semaphore(self, coro):
        async with self.semaphore:
            return await coro

    async def get_factor_values_over_instrument_list_async(
        self, instrument_list: list[Instrument], factor_name: str, lookback: int
    ) -> pd.DataFrame:
        try:
            tasks = []

            if factor_name == "skew":
                for instrument_code in instrument_list:
                    task = self.fetch_with_semaphore(
                        self.skew_handler.get_skew_async(instrument_code.symbol, factor_name=factor_name, lookback=lookback)
                    )
                    tasks.append(task)
            elif factor_name == "neg_skew":
                for instrument_code in instrument_list:
                    task = self.fetch_with_semaphore(
                        self.skew_handler.get_neg_skew_async(instrument_code.symbol, factor_name=factor_name, lookback=lookback)
                    )
                    tasks.append(task)
            else:
                raise ValueError("Invalid factor name. Only 'skew' and 'neg_skew' are supported.")

            # Gather all results concurrently, respecting the semaphore
            all_factor_values = await asyncio.gather(*tasks)

            # Build a DataFrame from the results
            instrument_symbols = [instrument.symbol for instrument in instrument_list]
            all_factor_values = pd.concat(all_factor_values, axis=1)
            all_factor_values.columns = instrument_symbols

            return all_factor_values

        except Exception:
            self.logger.exception("Error in processing factor values over instrument list")
            raise
