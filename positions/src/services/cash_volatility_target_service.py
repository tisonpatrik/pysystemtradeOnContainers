from common.src.logging.logger import AppLogger
from common.src.utils.constants import get_root_bdays_inyear


class CashVolTargetService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_daily_cash_vol_target(self, notional_trading_capital: float, percentage_vol_target: float) -> float:
        annual_cash_vol_target = self.get_annual_cash_vol_target(notional_trading_capital, percentage_vol_target)
        root_of_business_days_in_year = get_root_bdays_inyear()
        daily_cash_vol_target = annual_cash_vol_target / root_of_business_days_in_year

        return daily_cash_vol_target

    def get_annual_cash_vol_target(self, notional_trading_capital: float, percentage_vol_target: float) -> float:
        annual_cash_vol_target = notional_trading_capital * percentage_vol_target / 100.0
        return annual_cash_vol_target
