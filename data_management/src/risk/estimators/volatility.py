import numpy as np
import pandas as pd
import polars as pl
from polars import functions as pf
from src.core.dateutils import BUSINESS_DAYS_IN_YEAR


def robust_vol_calc(
    daily_returns: pl.DataFrame,
    days: int = 35,
    min_periods: int = 10,
    vol_abs_min: float = 0.0000000001,
    floor_min_quant: float = 0.05,
    floor_min_periods: int = 100,
    floor_days: int = 500,
) -> pl.DataFrame:
    """
    Robust exponential volatility calculation, assuming daily series of prices
    We apply an absolute minimum level of vol (absmin);
    and a volfloor based on lowest vol over recent history

    :param x: data
    :type x: Tx1 pd.Series

    :param days: Number of days in lookback (*default* 35)
    :type days: int

    :param min_periods: The minimum number of observations (*default* 10)
    :type min_periods: int

    :param vol_abs_min: The size of absolute minimum (*default* =0.0000000001)
      0.0= not used
    :type absmin: float or None

    :param vol_floor Apply a floor to volatility (*default* True)
    :type vol_floor: bool

    :param floor_min_quant: The quantile to use for volatility floor (eg 0.05
      means we use 5% vol) (*default 0.05)
    :type floor_min_quant: float

    :param floor_days: The lookback for calculating volatility floor, in days
      (*default* 500)
    :type floor_days: int

    :param floor_min_periods: Minimum observations for floor - until reached
      floor is zero (*default* 100)
    :type floor_min_periods: int

    :returns: pd.DataFrame -- volatility measure
    """

    # Standard deviation will be nan for first 10 non nan values
    serie = pl.Series(daily_returns)
    simple_vol = simple_ewvol_calc(serie, days=days, min_periods=min_periods)
    min_vol = apply_min_vol(simple_vol, vol_abs_min=vol_abs_min)
    vol = apply_vol_floor(
        min_vol,
        floor_min_quant=floor_min_quant,
        floor_min_periods=floor_min_periods,
        floor_days=floor_days,
    )

    return pl.DataFrame(vol)


def apply_min_vol(vol: pl.Series, vol_abs_min: float = 0.0000000001) -> pl.Series:
    vol[vol < vol_abs_min] = vol_abs_min

    return vol


def apply_vol_floor(
    vol: pl.Series,
    floor_min_quant: float = 0.05,
    floor_min_periods: int = 100,
    floor_days: int = 500,
) -> pl.Series:
    # Find the rolling 5% quantile point to set as a minimum
    vol_min = vol.rolling_quantile(
        min_periods=floor_min_periods, window_size=floor_days, quantile=floor_min_quant
    )
    # set this to zero for the first value then propagate forward, ensures
    # we always have a value
    vol_min[0] = 0.0
    minimal_volatility = vol_min.fill_null(strategy="forward")

    # apply the vol floor
    vol_floored = pl.Series(np.maximum(vol, vol_min))

    return vol_floored


def backfill_vol(vol: pl.Series) -> pl.Series:
    # Fill forwards first
    vol_forward_fill = vol.fill_null(strategy="forward")
    # Then backfill
    vol_backfilled = vol_forward_fill.fill_null(strategy="backward")

    return vol_backfilled


def mixed_vol_calc(
    daily_returns: pl.DataFrame,
    days: int = 35,
    min_periods: int = 10,
    slow_vol_years: int = 20,
    proportion_of_slow_vol: float = 0.35,
    vol_abs_min: float = 0.0000000001,
    backfill: bool = True,
) -> pl.DataFrame:
    # slow_vol_years can be also 20. need to be discovered
    """
    Robust exponential volatility calculation, assuming daily series of prices
    We apply an absolute minimum level of vol (absmin);
    and a volfloor based on lowest vol over recent history

    :param x: data
    :type x: Tx1 pd.Series

    :param days: Number of days in lookback (*default* 35)
    :type days: int

    :param min_periods: The minimum number of observations (*default* 10)
    :type min_periods: int

    :param vol_abs_min: The size of absolute minimum (*default* =0.0000000001)
      0.0= not used
    :type absmin: float or None

    :param vol_floor Apply a floor to volatility (*default* True)
    :type vol_floor: bool

    :param floor_min_quant: The quantile to use for volatility floor (eg 0.05
      means we use 5% vol) (*default 0.05)
    :type floor_min_quant: float

    :param floor_days: The lookback for calculating volatility floor, in days
      (*default* 500)
    :type floor_days: int

    :param floor_min_periods: Minimum observations for floor - until reached
      floor is zero (*default* 100)
    :type floor_min_periods: int

    :returns: pd.DataFrame -- volatility measure
    """
    serie = pl.Series(daily_returns)
    # Standard deviation will be nan for first 10 non nan values
    vol = simple_ewvol_calc(serie, days=days, min_periods=min_periods)
    slow_vol_days = slow_vol_years * BUSINESS_DAYS_IN_YEAR
    long_vol = vol.ewm_mean(slow_vol_days)
    prop_vol = long_vol * proportion_of_slow_vol + vol * (1 - proportion_of_slow_vol)
    min_vol = apply_min_vol(prop_vol, vol_abs_min=vol_abs_min)
    if backfill:
        # use the first vol in the past, sort of cheating
        min_vol = backfill_vol(min_vol)
    return pl.DataFrame(min_vol)


def simple_ewvol_calc(
    daily_returns: pl.Series, days: int = 35, min_periods: int = 10
) -> pl.Series:
    # Standard deviation will be nan for first 10 non nan values
    serie = pl.Series(daily_returns)
    vol = serie.ewm_std(span=days, adjust=True, min_periods=min_periods)

    return vol
