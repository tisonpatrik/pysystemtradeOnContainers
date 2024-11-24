import numpy as np
import pandas as pd

from common.logging.logger import AppLogger


class RelativeMomentumService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    def calculate_relative_momentum(
        self, normalised_price_this_instrument: pd.Series, normalised_price_for_asset_class: pd.Series, horizon: int
    ):
        try:
            ewma_span = int(horizon / 4.0)
            ewma_span = max(ewma_span, 2)

            outperformance = normalised_price_this_instrument.ffill() - normalised_price_for_asset_class.ffill()
            outperformance[outperformance == 0] = np.nan
            average_outperformance_over_horizon = (outperformance - outperformance.shift(horizon)) / horizon

            return average_outperformance_over_horizon.ewm(span=ewma_span).mean()
        except Exception as e:
            self.logger.exception("Error occurred in relative momentum calculation")
            raise ValueError("Failed to compute relative momentum due to invalid inputs or unexpected data issues.") from e
