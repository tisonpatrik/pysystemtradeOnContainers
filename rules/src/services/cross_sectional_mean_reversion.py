import pandas as pd

from common.src.logging.logger import AppLogger


class CSMeanReversionService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_cross_sectional_mean_reversion(
        self,
        normalised_price_this_instrument: pd.Series,
        normalised_price_for_asset_class: pd.Series,
        horizon: int,
    ) -> pd.Series:
        try:
            ewma_span = int(horizon / 4.0)
            ewma_span = max(ewma_span, 2)

            outperformance = (
                normalised_price_this_instrument.ffill()
                - normalised_price_for_asset_class.ffill()
            )
            relative_return = outperformance.diff()
            outperformance_over_horizon = relative_return.rolling(horizon).mean()

            return -outperformance_over_horizon.ewm(span=ewma_span).mean()
        except Exception as e:
            self.logger.exception("Error occurred in CrossSectionalMeanReversion calculation")
            error_message = "Failed to compute CSMeanReversion due to wrong inputs or unexpected data issues."
            raise ValueError(error_message) from e
