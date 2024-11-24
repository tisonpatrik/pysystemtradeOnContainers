import pandas as pd

from common.logging.logger import AppLogger


class CSMeanReversionService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_cross_sectional_mean_reversion(
        self,
        normalized_price_this_instrument: pd.Series,
        normalized_price_for_asset_class: pd.Series,
        horizon: int,
    ) -> pd.Series:
        try:
            ewma_span = int(horizon / 4.0)
            ewma_span = max(ewma_span, 2)

            outperformance = normalized_price_this_instrument.ffill() - normalized_price_for_asset_class.ffill()
            relative_return = outperformance.diff()
            outperformance_over_horizon = relative_return.rolling(horizon).mean()

            return -outperformance_over_horizon.ewm(span=ewma_span).mean()
        except Exception as e:
            self.logger.exception("Error occurred in CrossSectionalMeanReversion calculation")
            error_message = "Failed to compute CSMeanReversion due to wrong inputs or unexpected data issues."
            raise ValueError(error_message) from e
