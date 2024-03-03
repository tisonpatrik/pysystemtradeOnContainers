from src.app.models.risk_models import (
    DailyReturnsVolatility,
    DailyVolNormalisedPriceForAssetClass,
    DailyVolNormalizedReturns,
    InstrumentVolatility,
)
from src.services.risk.daily_returns_vol_seed_service import DailyReturnsVolSeedService
from src.services.risk.daily_vol_normalized_returns_seed_services import (
    DailyVolNormalisedReturnsSeedService,
)
from src.services.risk.instrument_vol_seed_service import InstrumentVolSeedService
from src.services.risk.normalised_price_for_asset_class_service import (
    NormalisedPriceForAssetClassService,
)

from common.logging.logger import AppLogger


class SeedRiskHandler:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_vol_seed_service = InstrumentVolSeedService(db_session)
        self.normalised_price_for_asset_seed_service = (
            NormalisedPriceForAssetClassService(db_session)
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
            DailyVolNormalisedPriceForAssetClass,
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
        elif model.__tablename__ == "daily_vol_normalised_price_for_asset_class":
            await self.normalised_price_for_asset_seed_service.seed_normalised_price_for_asset_class_async()
        else:
            raise ValueError(f"Unrecognized table name: {model.__tablename__}")
