import pandas as pd
from estimators.volatility import robust_vol_calc
from typing import Dict, Any

class EWMAComputer:
    def __init__(self, data: Dict[str, Any], speed: int):
        self.instrument = data['instrument']
        self.raw_data = data['raw_data']
        self.speed = speed

        self.validate_speed()
        self.validate_time_series_data()

        self.volatility = robust_vol_calc(self.raw_data)

    def validate_speed(self):
        if self.speed <= 0:
            raise ValueError("Speed should be a positive integer")

    def validate_time_series_data(self):
        if self.raw_data.empty:
            raise ValueError("Time series data cannot be empty")

    def compute_ewmac(self) -> pd.Series:
        Lfast = self.speed
        Lslow = self.speed * 4
        fast_ewma = self.raw_data.ewm(span=Lfast, min_periods=1).mean()
        slow_ewma = self.raw_data.ewm(span=Lslow, min_periods=1).mean()
        ewmac = fast_ewma - slow_ewma

        return ewmac / self.volatility.ffill()

    def process_data(self) -> Dict[str, Any]:
        ewmac = self.compute_ewmac()

        return {
            'message': 'EWMAC calculation and save completed successfully',
            'rule': 'MAC',
            'instrument': self.instrument,
            'speed': self.speed,
            'forecast': ewmac
        }
