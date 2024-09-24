import numpy as np
import pandas as pd

from common.src.utils.constants import get_bdays_inyear


def apply_min_vol(vol: pd.Series, vol_abs_min: float = 0.0000000001) -> pd.Series:
    vol[vol < vol_abs_min] = vol_abs_min

    return vol


def apply_vol_floor(
    vol: pd.Series,
    floor_min_quant: float = 0.05,
    floor_min_periods: int = 100,
    floor_days: int = 500,
) -> pd.Series:
    # Find the rolling 5% quantile point to set as a minimum
    vol_min = vol.rolling(min_periods=floor_min_periods, window=floor_days).quantile(q=floor_min_quant)

    # set this to zero for the first value then propagate forward, ensures
    # we always have a value
    vol_min.iloc[0] = 0.0
    vol_min = vol_min.bfill()

    # apply the vol floor
    return np.maximum(vol, vol_min)  # type: ignore


def backfill_vol(vol: pd.Series) -> pd.Series:
    # have to fill forwards first, as it's only the start we want to
    # backfill, eg before any value available

    vol_forward_fill = vol.ffill()
    return vol_forward_fill.bfill()


def mixed_vol_calc(  # noqa: PLR0913
    daily_returns: pd.Series,
    days: int = 35,
    min_periods: int = 10,
    slow_vol_years: int = 20,
    proportion_of_slow_vol: float = 0.35,
    vol_abs_min: float = 0.0000000001,
    backfill: bool = True,
) -> pd.Series:
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
    business_days_in_year = get_bdays_inyear()
    vol = simple_ewvol_calc(daily_returns, days=days, min_periods=min_periods)
    slow_vol_days = slow_vol_years * business_days_in_year
    long_vol = vol.ewm(span=slow_vol_days).mean()
    vol = long_vol * proportion_of_slow_vol + vol * (1 - proportion_of_slow_vol)
    vol = apply_min_vol(vol, vol_abs_min=vol_abs_min)
    if backfill:
        # use the first vol in the past, sort of cheating
        vol = backfill_vol(vol)
    return vol


def simple_ewvol_calc(daily_returns: pd.Series, days: int = 35, min_periods: int = 10) -> pd.Series:
    # Standard deviation will be nan for first 10 non nan values
    return daily_returns.ewm(adjust=True, span=days, min_periods=min_periods).std()


def daily_returns(daily_prices: pd.Series) -> pd.Series:
    return daily_prices.diff()
