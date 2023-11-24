import pandas as pd
from src.risk.estimators.volatility import mixed_vol_calc


def get_instrument_currency_vol(
    multiple_prices: pd.Series,
    adjusted_prices: pd.Series,
    point_size: float,
) -> pd.Series:
    block_value = get_block_value(multiple_prices, point_size)
    daily_perc_vol = get_daily_percentage_volatility(multiple_prices, adjusted_prices)
    ## FIXME WHY NOT RESAMPLE?
    (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")

    instr_ccy_vol = block_value.ffill() * daily_perc_vol

    return instr_ccy_vol


def get_block_value(
    underlying_price: pd.Series, value_of_price_move: float
) -> pd.Series:
    block_value = underlying_price.ffill() * value_of_price_move * 0.01
    return block_value


def get_daily_percentage_volatility(
    denom_price: pd.Series, daily_prices: pd.Series
) -> pd.Series:
    # Calculate the volatility of daily returns

    return_vol = daily_returns_volatility(daily_prices)
    (denom_price, return_vol) = denom_price.align(return_vol, join="right")
    perc_vol = 100.0 * (return_vol / denom_price.ffill().abs())

    return perc_vol


def daily_returns_volatility(daily_prices: pd.Series) -> pd.Series:
    """
    Calculates the daily returns volatility.
    """
    # Calculate daily returns
    price_returns = daily_returns(daily_prices)
    # Assuming mixed_vol_calc is adapted for Polars and returns a DataFrame
    # vol_multiplier can be adjusted as per your requirement
    vol_multiplier = 1
    raw_vol = mixed_vol_calc(price_returns)

    # Apply the multiplier to the volatility
    # Assuming 'volatility' is the column name in the raw_vol DataFrame
    vol = vol_multiplier * raw_vol

    return vol


def daily_returns(daily_prices: pd.Series) -> pd.Series:
    """
    Gets daily returns (not % returns)
    """
    dailyreturns = daily_prices.diff()
    return dailyreturns
