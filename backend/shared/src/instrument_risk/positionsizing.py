import pandas as pd
from shared.src.core.dateutils import ROOT_BDAYS_INYEAR
from shared.src.core.exceptions import missingData

def get_average_position_at_subsystem_level(self, instrument_code: str) -> pd.Series:
    """Get ratio of required volatility vs volatility of instrument in instrument's own currency.
    
    Parameters:
        instrument_code (str): Instrument to get values for.
        
    Returns:
        pd.Series: Tx1 pd.DataFrame.
    """
    instr_value_vol = get_instrument_value_vol(instrument_code)
    cash_vol_target = get_daily_cash_vol_target()
    
    vol_scalar = cash_vol_target / instr_value_vol
    
    return vol_scalar


def get_instrument_value_vol(self, instrument_code: str) -> pd.Series:
    """Get value of volatility of instrument in base currency (used for account value).
    
    Parameters:
        instrument_code (str): Instrument to get values for.
        
    Returns:
        pd.Series: Tx1 pd.DataFrame.
    """
    instr_ccy_vol = get_instrument_currency_vol(instrument_code)
    fx_rate = get_fx_rate(instrument_code)
    
    fx_rate = fx_rate.reindex(instr_ccy_vol.index, method="ffill")
    
    instr_value_vol = instr_ccy_vol.ffill() * fx_rate
    
    return instr_value_vol

def get_instrument_currency_vol(self, instrument_code: str) -> pd.Series:
    """Get value of volatility of instrument in instrument's own currency.
    
    Parameters:
        instrument_code (str): Instrument to get values for.
        
    Returns:
        pd.Series: Tx1 pd.DataFrame.
    """
    block_value = get_block_value(instrument_code)
    daily_perc_vol = get_price_volatility(instrument_code)

    # FIXME: WHY NOT RESAMPLE?
    block_value, daily_perc_vol = block_value.align(daily_perc_vol, join="inner")
    
    instr_ccy_vol = block_value.ffill() * daily_perc_vol

    return instr_ccy_vol

def get_block_value(self, instrument_code: str) -> pd.Series:
    """Calculate block value for instrument_code.
    
    Parameters:
        instrument_code (str): Instrument to get values for.
        
    Returns:
        pd.Series: Tx1 pd.DataFrame.
    """
    underlying_price = get_underlying_price(instrument_code)
    value_of_price_move = parent.data.get_value_of_block_price_move(instrument_code)
    
    block_value = underlying_price.ffill() * value_of_price_move * 0.01

    return block_value

def get_underlying_price(self, instrument_code: str) -> pd.Series:
    """Get various things from data and rawdata to calculate position sizes.
    
    KEY INPUT
    
    Parameters:
        instrument_code (str): Instrument to get values for.
        
    Returns:
        pd.Series: Tx1 pd.DataFrame: Underlying price [as used to work out % volatility].
    """
    try:
        rawdata = rawdata_stage
    except missingData:
        underlying_price = data.daily_prices(instrument_code)
    else:
        underlying_price = rawdata.daily_denominator_price(instrument_code)
    
    return underlying_price


def get_price_volatility(self, instrument_code: str) -> pd.Series:
    """Get the daily % volatility; If a rawdata stage exists from there; otherwise work it out.
    
    Parameters:
        instrument_code (str): Instrument to get values for.
        
    Returns:
        pd.Series: Tx1 pd.DataFrame.
        
    KEY INPUT
    
    Note:
        As an exception to the normal rule, we cache this, as it sometimes comes from data.
    """
    daily_perc_vol = get_daily_percentage_volatility(instrument_code)
    
    return daily_perc_vol

def get_vol_target_dict(self) -> dict:
    """Get the daily cash vol target.
    
    Requires: 
        - percentage_vol_target
        - notional_trading_capital
        - base_currency
        
    To find these, look in:
        (a) system.config.parameters,
        (b) if not found, in systems.get_defaults.py
        
    Returns:
        dict: A dictionary containing vol target information.
    """
    
    percentage_vol_target = get_percentage_vol_target()
    notional_trading_capital = get_notional_trading_capital()
    base_currency = get_base_currency()
    
    annual_cash_vol_target = annual_cash_vol_target()
    daily_cash_vol_target = get_daily_cash_vol_target()
    
    vol_target_dict = {
        'base_currency': base_currency,
        'percentage_vol_target': percentage_vol_target,
        'notional_trading_capital': notional_trading_capital,
        'annual_cash_vol_target': annual_cash_vol_target,
        'daily_cash_vol_target': daily_cash_vol_target
    }
    
    return vol_target_dict


def get_daily_cash_vol_target(self) -> float:
    """Get the daily cash vol target.
    
    Returns:
        float: The daily cash vol target.
    """
    annual_cash_vol_target = annual_cash_vol_target()
    daily_cash_vol_target = annual_cash_vol_target / ROOT_BDAYS_INYEAR
    
    return daily_cash_vol_target

def annual_cash_vol_target(self) -> float:
    notional_trading_capital = get_notional_trading_capital()
    percentage_vol_target = get_percentage_vol_target()

    annual_cash_vol_target = (
        notional_trading_capital * percentage_vol_target / 100.0
    )

    return annual_cash_vol_target


def get_notional_trading_capital(self) -> float:
    return float(config.notional_trading_capital)


def get_percentage_vol_target(self) -> float:
    return float(config.percentage_vol_target)


def get_base_currency(self) -> str:
    return config.base_currency


def get_fx_rate(self, instrument_code: str) -> pd.Series:
    """Get FX rate to translate instrument volatility into the same currency as account value.

    KEY INPUT

    Args:
        instrument_code (str): Instrument to get values for.

    Returns:
        pd.Series: Tx1 pd.DataFrame representing the fx rate.
    """
    base_currency = get_base_currency()
    fx_rate = data.get_fx_for_instrument(instrument_code, base_currency)

    return fx_rate
