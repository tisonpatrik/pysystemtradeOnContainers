# from common.src.logging.logger import AppLogger
# import pandas as pd

# class DailyAnnualisedRollHandler:
#     def __init__(self):
#         self.logger = AppLogger.get_instance().get_logger()

#     async def get_daily_annualised_roll_async(self, instrument_code: str)->pd.Series:
#         annroll = self.annualised_roll(instrument_code)
#         annroll = annroll.resample("1B").mean()
#         return annroll

#     def annualised_roll(self, instrument_code: str) -> pd.Series:
#             rolldiffs = self.roll_differentials(instrument_code)
#             rawrollvalues = self.raw_futures_roll(instrument_code)
#             annroll = rawrollvalues / rolldiffs
#             return annroll

#     def roll_differentials(self, instrument_code: str) -> pd.Series:
#         carrydata = self.get_instrument_raw_carry_data(instrument_code)
#         roll_diff = carrydata.roll_differentials()

#         return roll_diff

#     def roll_differentials(
#         self, floor_date_diff: float = 1 / CALENDAR_DAYS_IN_YEAR
#     ) -> pd.Series:
#         raw_differential = self.raw_differential()

#         ## This prevents the roll differential from being zero in a corner
#         ##     case when the two contract months match - it has to be at least one day

#         floored_differential = apply_abs_min(raw_differential, floor_date_diff)
#         unique_differential = uniquets(floored_differential)

#         return unique_differential


#     def raw_futures_roll(self, instrument_code: str) -> pd.Series:

#         carrydata = self.get_instrument_raw_carry_data(instrument_code)
#         raw_roll = carrydata.raw_futures_roll()

#         return raw_roll
