from src.core.utils.logging import AppLogger
from src.data_seeder.services.daily_returns_vol_seed_service import \
    DailyReturnsVolSeedService
from src.data_seeder.services.daily_vol_normalized_returns_seed_services import \
    DailyVolNormalisedReturnsSeedService
from src.data_seeder.services.instrument_vol_seed_service import \
    InstrumentVolSeedService
from src.data_seeder.services.normalised_price_for_asset_seed_service import \
    NormalisedPriceForAssetSeedService
from src.db.services.data_insert_service import DataInsertService
from src.risk.models.risk_models import (DailyReturnsVolatility,
                                         DailyVolNormalizedReturns,
                                         InstrumentVolatility,
                                         NormalisedPriceForAssetClass)


class SeedRiskHandler:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)
        self.instrument_vol_seed_service = InstrumentVolSeedService(db_session)
        self.normalised_price_for_asset_seed_service = (
            NormalisedPriceForAssetSeedService(db_session)
        )
        self.daily_returns_vol_seed_service = DailyReturnsVolSeedService(db_session)
        self.daily_returns_normalised_vol_seed_service = (
            DailyVolNormalisedReturnsSeedService(db_session)
        )

    async def seed_calculate_risk_data_async(self):
        """
        Asynchronously seed the database of risk calculations using predefined schemas.
        """
        self.logger.info("Data processing for risk calculations has started")
        models = [
            DailyReturnsVolatility,
            InstrumentVolatility,
            DailyVolNormalizedReturns,
            NormalisedPriceForAssetClass,
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
        elif model.__tablename__ == "daily_vol_normalized_returns":
            await self.daily_returns_normalised_vol_seed_service.seed_daily_normalised_returns_vol_async()
        elif model.__tablename__ == "normalised_price_for_asset_class":
            await self.normalised_price_for_asset_seed_service.seed_normalised_price_for_asset_class_async()
        else:
            raise ValueError(f"Unrecognized table name: {model.__tablename__}")
