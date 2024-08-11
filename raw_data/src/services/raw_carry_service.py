import numpy as np
import pandas as pd

from common.src.utils.constants import get_calendar_days_inyear
from common.src.utils.pd_utils import uniquets_series
from common.src.utils.strategy_functions import apply_abs_min

class RawCarryService:
    def __init__(self):
        self.floor_date_diff: float = 1 / get_calendar_days_inyear()

    def get_roll_differentials(self, raw_carry: pd.DataFrame) -> pd.Series:
        price_contract_as_frac = self._price_contract_as_year_frac(raw_carry)
        carry_contract_as_frac = self._carry_contract_as_year_frac(raw_carry)
        raw_differential = carry_contract_as_frac - price_contract_as_frac
        floored_differential = apply_abs_min(raw_differential, self.floor_date_diff)
        unique_differential = uniquets_series(floored_differential)

        return unique_differential

    def raw_futures_roll(self, raw_carry: pd.DataFrame) -> pd.Series:
        raw_roll = raw_carry.price - raw_carry.carry
        raw_roll[raw_roll == 0] = np.nan
        raw_roll = uniquets_series(raw_roll)

        return raw_roll

    def _price_contract_as_year_frac(self, raw_data: pd.DataFrame) -> pd.Series:
        price_contract_as_float = raw_data.price_contract.astype(float)
        price_contract_as_float = self._total_year_frac_from_contract_series(price_contract_as_float)
        return price_contract_as_float

    def _carry_contract_as_year_frac(self, raw_data: pd.DataFrame) -> pd.Series:
        carry_contract_as_float = raw_data.carry_contract.astype(float)
        carry_contract_as_float = self._total_year_frac_from_contract_series(carry_contract_as_float)
        return carry_contract_as_float

    def _total_year_frac_from_contract_series(self, contract_as_float: pd.Series) -> pd.Series:
        years_from_contract_series = contract_as_float.floordiv(10000)
        month_frac_contract_series = (contract_as_float.mod(10000) / 100.0) / 12

        return years_from_contract_series + month_frac_contract_series
