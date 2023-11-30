from src.core.utils.logging import AppLogger
from src.data_seeder.services.cumulative_vol_seed_service import (
    CumulativeVolSeedService,
)
from src.data_seeder.services.daily_returns_vol_seed_service import (
    DailyReturnsVolSeedService,
)
from src.data_seeder.services.instrument_vol_seed_service import (
    InstrumentVolSeedService,
)
from src.db.services.data_insert_service import DataInsertService
from src.risk.models.risk_models import (
    CumulativeDailyVolNormalizedReturns,
    DailyReturnsVolatility,
    InstrumentVolatility,
)


class RiskHandler:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)
        self.instrument_vol_seed_service = InstrumentVolSeedService(db_session)

        self.cumulative_vol_seed_service = CumulativeVolSeedService(db_session)
        self.daily_returns_vol_seed_service = DailyReturnsVolSeedService(db_session)

    async def seed_calculate_risk_data_async(self):
        """
        Asynchronously seed the database of risk calculations using predefined schemas.
        """
        self.logger.info("Data processing for risk calculations has started")
        models = [
            DailyReturnsVolatility,
            InstrumentVolatility,
            CumulativeDailyVolNormalizedReturns,
        ]

        for model in models:
            await self._get_risk_data_from_raw_file(model)

    async def _get_risk_data_from_raw_file(self, model):
        """
        Data processing for CSV files.
        """
        if model.__tablename__ == "daily_returns_volatility":
            await self.daily_returns_vol_seed_service.seed_daily_returns_vol_async()
        elif model.__tablename__ == "instrument_volatility":
            await self.instrument_vol_seed_service.seed_instrument_volatility_async()
        elif model.__tablename__ == "cumulative_daily_vol_normalized_returns":
            await self.cumulative_vol_seed_service.seed_cumulative_volatility_async()
        else:
            raise ValueError(f"Unrecognized table name: {model.__tablename__}")
