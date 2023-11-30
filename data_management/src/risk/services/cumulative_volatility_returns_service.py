from src.core.polars.prapare_db_calculations import prepara_data_to_db
from src.core.utils.logging import AppLogger
from src.db.services.data_insert_service import DataInsertService
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.errors.cumulative_volatility_returns_errors import (
    CumulativeVolatilityReturnsCalculationError,
)
from src.risk.estimators.cumulative_daily_vol_normalised_returns import (
    CumulativeDailyVolNormalisedReturns,
)
from src.risk.models.risk_models import CumulativeDailyVolNormalizedReturns


class CumulativeVolatilityReturnsService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.cumulative_daily_vol_normalised_returns = (
            CumulativeDailyVolNormalisedReturns()
        )
        self.table_name = CumulativeDailyVolNormalizedReturns.__tablename__
        self.data_insert_service = DataInsertService(db_session)

    async def insert_cumulative_vol_for_prices_async(self, daily_returns_vol, symbol):
        """Calculates and insert cumulative volatility of a given prices."""
        try:
            self.logger.info("Starting the cumulative vol for %s symbol.", symbol)
            cumulative_daily_returns = self.cumulative_daily_vol_normalised_returns.get_cumulative_daily_vol_normalised_returns(
                daily_returns_vol
            )
            prepared_data = prepara_data_to_db(
                cumulative_daily_returns, CumulativeDailyVolNormalizedReturns, symbol
            )
            await self.data_insert_service.async_insert_dataframe_to_table(
                prepared_data, self.table_name
            )
        except Exception as exc:
            self.logger.error(
                f"Error in calculating cumulative volatility returns: {exc}"
            )
            raise CumulativeVolatilityReturnsCalculationError()
