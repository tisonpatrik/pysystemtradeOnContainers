from common.src.logging.logger import AppLogger
from common.src.utils.constants import get_root_bdays_inyear


class CashVolTargetService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def get_daily_cash_vol_target(
        self, notional_trading_capital: float, percentage_vol_target: float
    ) -> float:
        try:
            annual_cash_vol_target = self.get_annual_cash_vol_target(
                notional_trading_capital, percentage_vol_target
            )
            root_of_business_days_in_year = get_root_bdays_inyear()
            if root_of_business_days_in_year == 0:
                self.logger.error("Division by zero error due to zero business days.")
                raise ValueError("Cannot divide by zero business days.")
            daily_cash_vol_target = (
                annual_cash_vol_target / root_of_business_days_in_year
            )
            return daily_cash_vol_target
        except (TypeError, ValueError) as e:
            self.logger.error(f"Error calculating daily cash volume target: {str(e)}")
            raise

    def get_annual_cash_vol_target(
        self, notional_trading_capital: float, percentage_vol_target: float
    ) -> float:
        if not isinstance(notional_trading_capital, (int, float)) or not isinstance(
            percentage_vol_target, (int, float)
        ):
            self.logger.error(
                "Invalid input types for notional_trading_capital or percentage_vol_target."
            )
            raise TypeError(
                "Both notional_trading_capital and percentage_vol_target must be numbers."
            )
        annual_cash_vol_target = (
            notional_trading_capital * percentage_vol_target / 100.0
        )
        return annual_cash_vol_target
