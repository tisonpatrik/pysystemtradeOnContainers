import pandas as pd

from common.src.logging.logger import AppLogger


class InstrumentVolService:
    def __init__(self) -> None:
        self.logger = AppLogger.get_instance().get_logger()

    def get_instrument_volatility(self, records: list, annual_cash_vol_target: float) -> pd.DataFrame:
        instr_value_vol = self._create_volatility_series(records)
        vol_scalar = self._calculate_volatility_scalar(instr_value_vol, annual_cash_vol_target)
        return vol_scalar

    def _create_volatility_series(self, instrument_volatility: list) -> pd.Series:
        df = pd.DataFrame(instrument_volatility)
        return pd.Series(data=df["instrument_volatility"].values, index=pd.to_datetime(df["date_time"]))

    def _calculate_volatility_scalar(self, instr_value_vol: pd.Series, annual_cash_vol_target: float) -> pd.DataFrame:
        vol_scalar = annual_cash_vol_target / instr_value_vol
        return pd.DataFrame(vol_scalar)
