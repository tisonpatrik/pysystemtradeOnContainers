import pandas as pd


class InstrumentCurrencyVolEstimator:

    def get_instrument_currency_vol(
        self,
        multiple_prices: pd.Series,
        daily_returns_vol: pd.Series,
        point_size: float,
    ) -> pd.Series:
        block_value = self.get_block_value(multiple_prices, point_size)
        daily_perc_vol = self.get_daily_percentage_volatility(multiple_prices, daily_returns_vol)
        ## FIXME WHY NOT RESAMPLE?
        (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")

        instr_ccy_vol = block_value.ffill() * daily_perc_vol
        return instr_ccy_vol

    def get_block_value(self, underlying_price: pd.Series, value_of_price_move: float) -> pd.Series:
        block_value = underlying_price.ffill() * value_of_price_move * 0.01
        return block_value

    def get_daily_percentage_volatility(self, denom_price: pd.Series, daily_returns_vol: pd.Series) -> pd.Series:
        # Calculate the volatility of daily returns
        (denom_price, return_vol) = denom_price.align(daily_returns_vol, join="right")
        perc_vol = 100.0 * (return_vol / denom_price.ffill().abs())

        return perc_vol
