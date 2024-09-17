from common.src.logging.logger import AppLogger
from common.src.utils.constants import get_root_bdays_inyear


class CashVolTargetService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_daily_cash_vol_target(self, notional_trading_capital: float, percentage_vol_target: float) -> float:
        try:
            annual_cash_vol_target = notional_trading_capital * percentage_vol_target / 100.0
            root_of_business_days_in_year = self._get_valid_root_bdays_inyear()
            return annual_cash_vol_target / root_of_business_days_in_year
        except (TypeError, ValueError):
            self.logger.exception("Error calculating daily cash volume target")
            raise

    def _get_valid_root_bdays_inyear(self) -> float:
        root_of_business_days_in_year = get_root_bdays_inyear()
        if root_of_business_days_in_year == 0:
            self.logger.error("Division by zero error due to zero business days.")
            raise ValueError("Cannot divide by zero business days.")
        return root_of_business_days_in_year
