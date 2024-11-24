import pandas as pd

from common.logging.logger import AppLogger


class InstrumentCurrencyVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_instrument_vol(self, denom_price: pd.Series, daily_perc_vol: pd.Series, point_size: float) -> pd.Series:
        try:
            block_value = denom_price.ffill() * point_size * 0.01
            ## FIXME WHY NOT RESAMPLE?
            (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")
            return block_value.ffill() * daily_perc_vol

        except Exception:
            self.logger.exception("Unexpected error occurred while calculating instrument volatility")
            raise
