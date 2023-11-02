import pandas as pd


def get_instrument_currency_vol(instrument_code: str) -> pd.Series:
    block_value = get_block_value(instrument_code)
    daily_perc_vol = get_price_volatility(instrument_code)

    ## FIXME WHY NOT RESAMPLE?
    (block_value, daily_perc_vol) = block_value.align(daily_perc_vol, join="inner")

    instr_ccy_vol = block_value.ffill() * daily_perc_vol

    return instr_ccy_vol


def get_block_value(instrument_code: str) -> pd.Series:
    underlying_price = get_underlying_price(instrument_code)
    value_of_price_move = get_value_of_block_price_move(instrument_code)

    block_value = underlying_price.ffill() * value_of_price_move * 0.01

    return block_value


def get_price_volatility(instrument_code: str) -> pd.Series:
    daily_perc_vol = get_daily_percentage_volatility(instrument_code)

    return daily_perc_vol


def get_underlying_price(instrument_code: str) -> pd.Series:
    underlying_price = daily_denominator_price(instrument_code)
    return underlying_price


def daily_denominator_price(instrument_code: str) -> pd.Series:
    prices = get_instrument_raw_carry_data(instrument_code).PRICE  # get multiple prices
    daily_prices = prices.resample("1B").last()
    return daily_prices


def get_value_of_block_price_move(instrument_code: str) -> float:
    """
    How much is a $1 move worth in value terms?

    :param instrument_code: instrument to get value for
    :type instrument_code: str

    :returns: float

    """

    instr_object = get_instrument_object_with_meta_data(
        instrument_code
    )  # get instrument config table
    meta_data = instr_object.meta_data
    block_move_value = meta_data.Pointsize

    return block_move_value


def get_daily_percentage_volatility(instrument_code: str) -> pd.Series:
    denom_price = daily_denominator_price(instrument_code)
    return_vol = daily_returns_volatility(instrument_code)
    (denom_price, return_vol) = denom_price.align(return_vol, join="right")
    perc_vol = 100.0 * (return_vol / denom_price.ffill().abs())

    return perc_vol


def daily_returns_volatility(instrument_code: str) -> pd.Series:
    volconfig = copy(self.config.volatility_calculation)

    price_returns = daily_returns(instrument_code)

    # volconfig contains 'func' and some other arguments
    # we turn func which could be a string into a function, and then
    # call it with the other ags
    vol_multiplier = volconfig.pop("multiplier_to_get_daily_vol")

    volfunction = resolve_function(volconfig.pop("func"))
    raw_vol = volfunction(price_returns, **volconfig)  # vol.mixed_vol_calc

    vol = vol_multiplier * raw_vol

    return vol


def daily_returns(instrument_code: str) -> pd.Series:
    """
    Gets daily returns (not % returns)

    :param instrument_code: Instrument to get prices for
    :type trading_rules: str

    :returns: Tx1 pd.DataFrame


    >>> from systems.tests.testdata import get_test_object
    >>> from systems.basesystem import System
    >>>
    >>> (rawdata, data, config)=get_test_object()
    >>> system=System([rawdata], data)
    >>> system.rawdata.daily_returns("SOFR").tail(2)
                    price
    2015-12-10 -0.0650
    2015-12-11  0.1075
    """
    instrdailyprice = get_daily_prices(instrument_code)
    dailyreturns = instrdailyprice.diff()

    return dailyreturns


def get_daily_prices(instrument_code) -> pd.Series:
    """
    Gets daily prices

    :param instrument_code: Instrument to get prices for
    :type trading_rules: str

    :returns: Tx1 pd.DataFrame

    KEY OUTPUT
    """

    dailyprice = daily_prices(instrument_code)  # adjusted prices

    if len(dailyprice) == 0:
        raise Exception(
            "Data for %s not found! Remove from instrument list, or add to config.ignore_instruments"
            % instrument_code
        )

    return dailyprice
