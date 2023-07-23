import pandas as pd
import numpy as np
from typing import Dict, Any
from rule import Rule

class BreakoutComputer(Rule):
    def __init__(self, data: Dict[str, Any], speed: int):
        super().__init__(data)
        self.speed = speed
        self.validate_speed(speed)

    def compute_breakdown(self, smooth=None) -> pd.Series:
        if smooth is None:
            smooth = max(int(self.speed / 4.0), 1)

        assert smooth < self.speed

        roll_max = self.raw_data.rolling(
            self.speed, min_periods=int(min(len(self.raw_data), np.ceil(self.speed / 2.0)))
        ).max()
        roll_min = self.raw_data.rolling(
            self.speed, min_periods=int(min(len(self.raw_data), np.ceil(self.speed / 2.0)))
        ).min()

        roll_mean = (roll_max + roll_min) / 2.0

        output = 40.0 * ((self.raw_data - roll_mean) / (roll_max - roll_min))
        smoothed_output = output.ewm(span=smooth, min_periods=np.ceil(smooth / 2.0)).mean()

        return smoothed_output

    def process_data(self) -> Dict[str, Any]:
        breakdown = self.compute_breakdown()

        return {
            'message': 'Breakdown calculation and save completed successfully',
            'rule': 'Breakdown',
            'instrument': self.instrument,
            'speed': self.speed,
            'forecast': breakdown
        }
