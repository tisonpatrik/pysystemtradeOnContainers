import polars as pl
from src.risk.estimators.volatility import mixed_vol_calc


def get_instrument_currency_vol(
    multiple_prices: pl.DataFrame, adjusted_prices: pl.DataFrame, point_size: float
) -> pl.DataFrame:
    block_value = get_block_value(multiple_prices, point_size)
    daily_perc_vol = get_daily_percentage_volatility(multiple_prices, adjusted_prices)
    ## FIXME WHY NOT RESAMPLE?
    (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")

    instr_ccy_vol = block_value.ffill() * daily_perc_vol
    return instr_ccy_vol


def get_block_value(
    underlying_price: pl.DataFrame, value_of_price_move: float
) -> pl.DataFrame:
    filled = underlying_price.fill_null(strategy="forward")
    block_value = filled * value_of_price_move * 0.01

    return block_value


def get_daily_percentage_volatility(
    denom_price: pl.DataFrame, daily_prices: pl.DataFrame
) -> pl.DataFrame:
    # Calculate the volatility of daily returns
    return_vol = daily_returns_volatility(daily_prices)
    combined_df = denom_price.join(return_vol, on="key_column", how="inner")
    denom_price_ffilled = combined_df.fill_null(strategy="forward")
    serie = denom_price_ffilled.to_series().abs()
    perc_vol = 100.0 * (return_vol / serie)

    return perc_vol


def daily_returns_volatility(daily_prices: pl.DataFrame) -> pl.DataFrame:
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
    vol = raw_vol.select(pl.col("volatility") * vol_multiplier)

    return vol


def daily_returns(daily_prices: pl.DataFrame) -> pl.DataFrame:
    """
    Gets daily returns (not % returns)
    """
    # Assuming 'price' is the column with daily prices
    dailyreturns = daily_prices.select(pl.col("price").diff().alias("price"))

    return dailyreturns
