# import pandas as pd
# from shared.src.estimators.volatility import robust_vol_calc
# from typing import Dict, Any
# from shared.src.rules.rule import Rule


# class EWMAComputer(Rule):
#     def __init__(self, data: Dict[str, Any], speed: int):
#         super().__init__(data)
#         self.speed = speed
#         self.validate_speed(speed)

#     def compute_ewmac(self) -> pd.Series:
#         Lfast = self.speed
#         Lslow = self.speed * 4
#         fast_ewma = self.raw_data.ewm(span=Lfast, min_periods=1).mean()
#         slow_ewma = self.raw_data.ewm(span=Lslow, min_periods=1).mean()
#         return fast_ewma - slow_ewma

#     def process_data(self) -> Dict[str, Any]:
#         ewmac = self.compute_ewmac()
#         volatility = robust_vol_calc(self.raw_data)
#         forecast = ewmac / volatility.ffill()

#         return {
#             "message": "EWMAC calculation and save completed successfully",
#             "rule": "MAC",
#             "instrument": self.instrument,
#             "speed": self.speed,
#             "forecast": forecast,
#         }
