import pandas as pd

from common.src.utils.constants import get_calendar_days_inyear
from common.src.utils.pd_utils import uniquets_series
from common.src.utils.strategy_functions import apply_abs_min
from raw_data.utils.carry import carry_contract_as_year_frac, price_contract_as_year_frac


class RawCarryService:
    def __init__(self):
        self.floor_date_diff: float = 1 / get_calendar_days_inyear()

    def get_roll_differentials(self, raw_carry: pd.DataFrame) -> pd.Series:
        price_contract_as_frac = price_contract_as_year_frac(raw_carry)
        carry_contract_as_frac = carry_contract_as_year_frac(raw_carry)
        raw_differential = carry_contract_as_frac - price_contract_as_frac
        floored_differential = apply_abs_min(raw_differential, self.floor_date_diff)
        unique_differential = uniquets_series(floored_differential)
        return pd.Series(data=unique_differential.values, index=raw_carry.time)
