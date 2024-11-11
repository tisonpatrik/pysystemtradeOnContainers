import pandas as pd

from common.src.logging.logger import AppLogger


class InstrumentCurrencyVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_instrument_vol_async(self, denom_price: pd.Series, daily_returns_vol: pd.Series, point_size: float) -> pd.Series:
        try:
            block_value = denom_price.ffill() * point_size * 0.01
            daily_perc_vol = self.get_daily_percentage_volatility(denom_price, daily_returns_vol)
            ## FIXME WHY NOT RESAMPLE?
            (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")

            return block_value.ffill() * daily_perc_vol

        except Exception:
            self.logger.exception("Unexpected error occurred while calculating instrument volatility")
            raise

    def get_daily_percentage_volatility(self, denom_price: pd.Series, daily_returns_vol: pd.Series) -> pd.Series:
        # Calculate the volatility of daily returns
        (denom_price, return_vol) = denom_price.align(daily_returns_vol, join="right")
        return 100.0 * (return_vol / denom_price.ffill().abs())
