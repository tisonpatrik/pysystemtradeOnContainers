# from copy import copy

# import pandas as pd

# from syscore.objects import resolve_function
# from shared.src.core.dateutils import ROOT_BDAYS_INYEAR
# from shared.src.core.genutils import list_intersection
# from shared.src.core.exceptions import missingData

# from sysdata.sim.futures_sim_data import futuresSimData
# from sysdata.config.configdata import Config

# from sysobjects.carry_data import rawCarryData


# def get_daily_prices(self, instrument_code) -> pd.Series:
#     """
#     Gets daily prices

#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame

#     KEY OUTPUT
#     """

#     dailyprice = self.data_stage.daily_prices(instrument_code)

#     if len(dailyprice) == 0:
#         raise Exception(
#             "Data for %s not found! Remove from instrument list, or add to config.ignore_instruments"
#             % instrument_code
#         )

#     return dailyprice


# def get_natural_frequency_prices(self, instrument_code: str) -> pd.Series:

#     natural_prices = self.data_stage.get_raw_price(instrument_code)

#     if len(natural_prices) == 0:
#         raise Exception(
#             "Data for %s not found! Remove from instrument list, or add to config.ignore_instruments"
#         )

#     return natural_prices


# def get_hourly_prices(self, instrument_code: str) -> pd.Series:
#     hourly_prices = self.data_stage.hourly_prices(instrument_code)

#     return hourly_prices


# def daily_returns(self, instrument_code: str) -> pd.Series:
#     """
#     Gets daily returns (not % returns)

#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame
#     """
#     instrdailyprice = self.get_daily_prices(instrument_code)
#     dailyreturns = instrdailyprice.diff()

#     return dailyreturns


# def hourly_returns(self, instrument_code: str) -> pd.Series:
#     """
#     Gets hourly returns (not % returns)

#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame


#     """
#     hourly_prices = self.get_hourly_prices(instrument_code)
#     hourly_returns = hourly_prices.diff()

#     return hourly_returns


# def annualised_returns_volatility(self, instrument_code: str) -> pd.Series:
#     daily_returns_volatility = self.daily_returns_volatility(
#         instrument_code)

#     return daily_returns_volatility * ROOT_BDAYS_INYEAR


# def daily_returns_volatility(self, instrument_code: str) -> pd.Series:
#     """
#     Gets volatility of daily returns (not % returns)

#     This is done using a user defined function

#     We get this from:
#       the configuration object
#       or if not found, system.defaults.py

#     The dict must contain func key; anything else is optional

#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame
#     """
#     volconfig = copy(self.config.volatility_calculation)

#     which_returns = volconfig.pop("name_returns_attr_in_rawdata")
#     returns_func = getattr(self, which_returns)
#     price_returns = returns_func(instrument_code)

#     # volconfig contains 'func' and some other arguments
#     # we turn func which could be a string into a function, and then
#     # call it with the other ags
#     vol_multiplier = volconfig.pop("multiplier_to_get_daily_vol")

#     volfunction = resolve_function(volconfig.pop("func"))
#     raw_vol = volfunction(price_returns, **volconfig)

#     vol = vol_multiplier * raw_vol

#     return vol


# def get_daily_percentage_returns(self, instrument_code: str) -> pd.Series:
#     """
#     Get percentage returns

#     Useful statistic, also used for some trading rules

#     This is an optional subsystem; forecasts can go straight to system.data
#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame
#     """

#     # UGLY
#     denom_price = self.daily_denominator_price(instrument_code)
#     num_returns = self.daily_returns(instrument_code)
#     perc_returns = num_returns / denom_price.ffill()

#     return perc_returns


# def get_daily_percentage_volatility(self, instrument_code: str) -> pd.Series:
#     """
#     Get percentage returns normalised by recent vol

#     Useful statistic, also used for some trading rules

#     This is an optional subsystem; forecasts can go straight to system.data
#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame
#     """
#     denom_price = self.daily_denominator_price(instrument_code)
#     return_vol = self.daily_returns_volatility(instrument_code)
#     (denom_price, return_vol) = denom_price.align(return_vol, join="right")
#     perc_vol = 100.0 * (return_vol / denom_price.ffill().abs())

#     return perc_vol


# def get_daily_vol_normalised_returns(self, instrument_code: str) -> pd.Series:
#     """
#     Get returns normalised by recent vol

#     Useful statistic, also used for some trading rules

#     This is an optional subsystem; forecasts can go straight to system.data
#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame
#     """
#     returnvol = self.daily_returns_volatility(instrument_code).shift(1)
#     dailyreturns = self.daily_returns(instrument_code)
#     norm_return = dailyreturns / returnvol

#     return norm_return


# def get_cumulative_daily_vol_normalised_returns(
#     self, instrument_code: str
# ) -> pd.Series:
#     """
#     Returns a cumulative normalised return. This is like a price, but with equal expected vol
#     Used for a few different trading rules

#     :param instrument_code: str
#     :return: pd.Series
#     """
#     norm_returns = self.get_daily_vol_normalised_returns(instrument_code)

#     cum_norm_returns = norm_returns.cumsum()

#     return cum_norm_returns


# def _aggregate_daily_vol_normalised_returns_for_list_of_instruments(
#     self, list_of_instruments: list
# ) -> pd.Series:
#     """
#     Average normalised returns across an asset class

#     :param asset_class: str
#     :return: pd.Series
#     """

#     aggregate_returns_across_instruments_list = [
#         self.get_daily_vol_normalised_returns(instrument_code)
#         for instrument_code in list_of_instruments
#     ]

#     aggregate_returns_across_instruments = pd.concat(
#         aggregate_returns_across_instruments_list, axis=1
#     )

#     # we don't ffill before working out the median as this could lead to
#     # bad data
#     median_returns = aggregate_returns_across_instruments.median(axis=1)

#     return median_returns


# def _daily_vol_normalised_price_for_list_of_instruments(
#     self, list_of_instruments: list
# ) -> pd.Series:

#     norm_returns = (
#         self._aggregate_daily_vol_normalised_returns_for_list_of_instruments(
#             list_of_instruments
#         )
#     )
#     norm_price = norm_returns.cumsum()

#     return norm_price


# def _by_asset_class_daily_vol_normalised_price_for_asset_class(
#     self, asset_class: str
# ) -> pd.Series:
#     """
#     Price for an asset class, built up from cumulative returns

#     :param asset_class: str
#     :return: pd.Series
#     """

#     instruments_in_asset_class = self.all_instruments_in_asset_class(
#         asset_class)

#     norm_price = self._daily_vol_normalised_price_for_list_of_instruments(
#         instruments_in_asset_class
#     )

#     return norm_price


# def normalised_price_for_asset_class(self, instrument_code: str) -> pd.Series:
#     """
#     :param instrument_code:
#     :return:
#     """
#     asset_class = self.data_stage.asset_class_for_instrument(
#         instrument_code)
#     normalised_price_for_asset_class = (
#         self._by_asset_class_daily_vol_normalised_price_for_asset_class(
#             asset_class)
#     )
#     normalised_price_this_instrument = (
#         self.get_cumulative_daily_vol_normalised_returns(instrument_code)
#     )

#     # Align for an easy life
#     # As usual forward fill at last moment
#     normalised_price_for_asset_class_aligned = (
#         normalised_price_for_asset_class.reindex(
#             normalised_price_this_instrument.index
#         ).ffill()
#     )

#     return normalised_price_for_asset_class_aligned


# def rolls_per_year(self, instrument_code: str) -> int:
#     # an input but we cache to avoid spamming with errors
#     try:
#         rolls_per_year = self.data_stage.get_rolls_per_year(
#             instrument_code)
#     except:
#         self.log.warning(
#             "No roll data for %s, this is fine for spot instruments but not for futures"
#             % instrument_code
#         )
#         rolls_per_year = 0

#     return rolls_per_year


# def get_instrument_raw_carry_data(self, instrument_code: str) -> rawCarryData:
#     """
#     Returns the 4 columns PRICE, CARRY, PRICE_CONTRACT, CARRY_CONTRACT

#     :param instrument_code: instrument to get data for
#     :type instrument_code: str

#     :returns: Tx4 pd.DataFrame

#     KEY INPUT
#     """

#     instrcarrydata = self.data_stage.get_instrument_raw_carry_data(
#         instrument_code)
#     if len(instrcarrydata) == 0:
#         raise missingData(
#             "Data for %s not found! Remove from instrument list, or add to config.ignore_instruments"
#             % instrument_code
#         )

#     instrcarrydata = rawCarryData(instrcarrydata)

#     return instrcarrydata


# def raw_futures_roll(self, instrument_code: str) -> pd.Series:
#     """
#     Returns the raw difference between price and carry

#     :param instrument_code: instrument to get data for
#     :type instrument_code: str

#     :returns: Tx4 pd.DataFrame
#     """
#     carrydata = self.get_instrument_raw_carry_data(instrument_code)
#     raw_roll = carrydata.raw_futures_roll()

#     return raw_roll


# def roll_differentials(self, instrument_code: str) -> pd.Series:
#     """
#     Work out the annualisation factor

#     :param instrument_code: instrument to get data for
#     :type instrument_code: str

#     :returns: Tx4 pd.DataFrame
#     """
#     carrydata = self.get_instrument_raw_carry_data(instrument_code)
#     roll_diff = carrydata.roll_differentials()

#     return roll_diff


# def annualised_roll(self, instrument_code: str) -> pd.Series:
#     """
#     Work out annualised futures roll

#     :param instrument_code: instrument to get data for
#     :type instrument_code: str

#     :returns: Tx4 pd.DataFrame
#     """
#     rolldiffs = self.roll_differentials(instrument_code)
#     rawrollvalues = self.raw_futures_roll(instrument_code)

#     annroll = rawrollvalues / rolldiffs

#     return annroll


# def daily_annualised_roll(self, instrument_code: str) -> pd.Series:
#     """
#     Resample annualised roll to daily frequency

#     We don't resample earlier, or we'll get bad data

#     :param instrument_code: instrument to get data for
#     :type instrument_code: str

#     :returns: Tx1 pd.DataFrame
#     """

#     annroll = self.annualised_roll(instrument_code)
#     annroll = annroll.resample("1B").mean()

#     return annroll


# def raw_carry(self, instrument_code: str) -> pd.Series:
#     """
#     Returns the raw carry (annualised roll, divided by annualised vol)
#     Only thing needed now is smoothing, that is done in the actual trading rule

#     Added to rawdata to support relative carry trading rule

#     :param instrument_code:

#     :return: Tx1 pd.DataFrame
#     """

#     daily_ann_roll = self.daily_annualised_roll(instrument_code)
#     vol = self.daily_returns_volatility(instrument_code)

#     ann_stdev = vol * ROOT_BDAYS_INYEAR
#     raw_carry = daily_ann_roll / ann_stdev

#     return raw_carry


# def smoothed_carry(self, instrument_code: str, smooth_days: int = 90) -> pd.Series:
#     """
#     Returns the smoothed raw carry
#     Added to rawdata to support relative carry trading rule

#     :param instrument_code:

#     :return: Tx1 pd.DataFrame
#     """

#     raw_carry = self.raw_carry(instrument_code)
#     smooth_carry = raw_carry.ewm(smooth_days).mean()

#     return smooth_carry


# def _by_asset_class_median_carry_for_asset_class(
#     self, asset_class: str, smooth_days: int = 90
# ) -> pd.Series:
#     """

#     :param asset_class:
#     :return:
#     """

#     instruments_in_asset_class = self.all_instruments_in_asset_class(
#         asset_class)

#     raw_carry_across_asset_class = [
#         self.raw_carry(instrument_code)
#         for instrument_code in instruments_in_asset_class
#     ]

#     raw_carry_across_asset_class_pd = pd.concat(
#         raw_carry_across_asset_class, axis=1
#     )

#     smoothed_carrys_across_asset_class = raw_carry_across_asset_class_pd.ewm(
#         smooth_days
#     ).mean()

#     # we don't ffill before working out the median as this could lead to
#     # bad data
#     median_carry = smoothed_carrys_across_asset_class.median(axis=1)

#     return median_carry


# def median_carry_for_asset_class(self, instrument_code: str) -> pd.Series:
#     """
#     Median carry for the asset class relating to a given instrument
#     :param instrument_code: str
#     :return: pd.Series
#     """

#     asset_class = self.data_stage.asset_class_for_instrument(
#         instrument_code)
#     median_carry = self._by_asset_class_median_carry_for_asset_class(
#         asset_class)
#     instrument_carry = self.raw_carry(instrument_code)

#     # Align for an easy life
#     # As usual forward fill at last moment
#     median_carry = median_carry.reindex(instrument_carry.index).ffill()

#     return median_carry

# # sys.data.get_instrument_asset_classes()


# def daily_denominator_price(self, instrument_code: str) -> pd.Series:
#     """
#     Gets daily prices for use with % volatility
#     This won't always be the same as the normal 'price'

#     :param instrument_code: Instrument to get prices for
#     :type trading_rules: str

#     :returns: Tx1 pd.DataFrame

#     KEY OUTPUT
#     """
#     try:
#         prices = self.get_instrument_raw_carry_data(instrument_code).PRICE
#     except missingData:
#         self.log.warning(
#             "No carry data found for %s, using adjusted prices to calculate percentage returns"
#             % instrument_code
#         )
#         return self.get_daily_prices(instrument_code)

#     daily_prices = prices.resample("1B").last()

#     return daily_prices


# def all_instruments_in_asset_class(self, asset_class: str) -> list:
#     instruments_in_asset_class = self.data_stage.all_instruments_in_asset_class(
#         asset_class
#     )
#     instrument_list = self.instrument_list()
#     instruments_in_asset_class_and_master_list = list_intersection(
#         instruments_in_asset_class, instrument_list
#     )

#     return instruments_in_asset_class_and_master_list


# def instrument_list(self) -> list:
#     instrument_list = self.parent.get_instrument_list()
#     return instrument_list
