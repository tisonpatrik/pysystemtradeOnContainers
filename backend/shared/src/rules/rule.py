# from abc import ABC, abstractmethod
# from typing import Dict, Any
# import pandas as pd

# class Rule(ABC):
#     def __init__(self, data: Dict[str, Any]):
#         self.instrument = data['instrument']
#         self.raw_data = data['raw_data']
#         self.validate_time_series_data()

#     def validate_time_series_data(self):
#         if self.raw_data.empty:
#             raise ValueError("Time series data cannot be empty")

#     @abstractmethod
#     def process_data(self) -> Dict[str, Any]:
#         pass

#     # This can be overridden by child classes if needed
#     def validate_speed(self, speed: int):
#         if speed <= 0:
#             raise ValueError("Speed should be a positive integer")
