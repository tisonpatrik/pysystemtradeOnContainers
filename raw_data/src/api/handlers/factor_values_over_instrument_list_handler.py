import pandas as pd

from common.src.logging.logger import AppLogger
from common.src.validation.instrument import Instrument
from raw_data.src.api.handlers.skew_handler import SkewHandler
from raw_data.src.validation.factor_name import FactorName


class FactorValuesOverInstrumentListHandler:
    def __init__(self, skew_handler: SkewHandler):
        self.logger = AppLogger.get_instance().get_logger()
        self.skew_handler = skew_handler

    async def get_factor_values_over_instrument_list_async(
        self, instrument_list: list[Instrument], factor_name: FactorName, lookback: int
    ) -> pd.DataFrame:
        try:
            if factor_name.name == "skew":
                all_factor_values = [
                    await self.skew_handler.get_skew_async(instrument_code.symbol, factor_name=factor_name, lookback=lookback)
                    for instrument_code in instrument_list
                ]
            elif factor_name.name == "neg_skew":
                all_factor_values = [
                    await self.skew_handler.get_neg_skew_async(instrument_code.symbol, factor_name=factor_name, lookback=lookback)
                    for instrument_code in instrument_list
                ]
            else:
                raise ValueError("Invalid factor name. Only 'skew' and 'neg_skew' are supported.")
            instrument_symbols = [instrument.symbol for instrument in instrument_list]
            all_factor_values = pd.concat(all_factor_values, axis=1)
            all_factor_values.columns = instrument_symbols

            return all_factor_values
        except Exception:
            self.logger.exception("Error in processing factor values over instrument list")
            raise
