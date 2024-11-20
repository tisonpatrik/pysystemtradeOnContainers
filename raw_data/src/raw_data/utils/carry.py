import numpy as np
import pandas as pd

from common.src.utils.constants import get_root_bdays_inyear
from common.src.utils.pd_utils import uniquets_series


def get_raw_carry(daily_ann_roll: pd.Series, daily_returns_vol: pd.Series) -> pd.Series:
    ann_stdev = daily_returns_vol * get_root_bdays_inyear()
    return daily_ann_roll / ann_stdev


def raw_futures_roll(raw_carry: pd.DataFrame) -> pd.Series:
    raw_roll = raw_carry.price - raw_carry.carry
    raw_roll = pd.Series(data=raw_roll.values, index=raw_carry.time)
    raw_roll[raw_roll == 0] = np.nan
    return uniquets_series(raw_roll)


def price_contract_as_year_frac(raw_data: pd.DataFrame) -> pd.Series:
    price_contract_as_float = raw_data.price_contract.astype(float)
    return total_year_frac_from_contract_series(price_contract_as_float)


def carry_contract_as_year_frac(raw_data: pd.DataFrame) -> pd.Series:
    carry_contract_as_float = raw_data.carry_contract.astype(float)
    return total_year_frac_from_contract_series(carry_contract_as_float)


def total_year_frac_from_contract_series(contract_as_float: pd.Series) -> pd.Series:
    years_from_contract_series = contract_as_float.floordiv(10000)
    month_frac_contract_series = (contract_as_float.mod(10000) / 100.0) / 12

    return years_from_contract_series + month_frac_contract_series
