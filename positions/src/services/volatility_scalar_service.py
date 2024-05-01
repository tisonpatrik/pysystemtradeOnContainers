import pandas as pd

from common.src.logging.logger import AppLogger


class VolatilityScalarService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_volatility_scalar(self, cash_vol_target: float, instr_value_vol: pd.Series) -> pd.Series:
        vol_scalar = cash_vol_target / instr_value_vol
        return vol_scalar
