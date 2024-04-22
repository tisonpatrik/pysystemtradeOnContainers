import pandas as pd
from pandera.typing import DataFrame

from common.src.logging.logger import AppLogger
from risk.src.schemas.risk_schemas import CumulativeVolNormalizedReturnsSchema, DailyVolNormalizedReturnsSchema


class CumulativeDailyVolatilityNormalisedReturnsService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()
        self.validator = CumulativeVolNormalizedReturnsSchema

    def calculate_cumulative_vol_for_prices(
        self, daily_vol_normalised_returns: DataFrame[DailyVolNormalizedReturnsSchema]
    ) -> DataFrame[CumulativeVolNormalizedReturnsSchema]:
        """
        Calculate cumulative returns volatility by symbol and returns them as Pandas Series.
        """
        try:
            # SELECT id, hodnota, SUM(hodnota) OVER (ORDER BY id) AS cumsum FROM   tabulka;
            cum_norm_returns = daily_vol_normalised_returns.cumsum()
            df = pd.DataFrame(cum_norm_returns)
            returns = CumulativeVolNormalizedReturnsSchema.validate(df)
            return returns  # type: ignore

        except Exception as error:
            error_message = f"An error occurred during the processing: {error}"
            self.logger.error(error_message)
            raise ValueError(error_message)
