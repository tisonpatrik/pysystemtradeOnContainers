from src.services.risk.seed_daily_returns_vol_service import SeedDailyReturnsVolService
from src.services.risk.seed_daily_vol_normalised_price_for_asset_class_service import (
    SeedDailyVolNormalisedPriceForAssetClassService,
)
from src.services.risk.seed_daily_vol_normalised_returns_service import SeedDailyVolNormalisedReturnsService
from src.services.risk.seed_instrument_vol_service import SeedInstrumentVolService

from common.src.logging.logger import AppLogger
from risk.src.models.risk_models import (
    DailyReturnsVolModel,
    DailyVolNormalisedPriceForAssetClassModel,
    DailyVolNormalizedReturnsModel,
    InstrumentVolModel,
)


class SeedRiskDataHandler:
    def __init__(
        self,
        seed_daily_returns_vol_service: SeedDailyReturnsVolService,
        seed_instrument_vol_service: SeedInstrumentVolService,
        seed_daily_vol_normalised_returns_service: SeedDailyVolNormalisedReturnsService,
        seed_daily_vol_normalised_price_for_asset_class_service: SeedDailyVolNormalisedPriceForAssetClassService,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.seed_daily_returns_vol_service = seed_daily_returns_vol_service
        self.seed_instrument_vol_service = seed_instrument_vol_service
        self.seed_daily_vol_normalised_returns_service = seed_daily_vol_normalised_returns_service
        self.seed_daily_vol_normalised_price_for_asset_class_service = (
            seed_daily_vol_normalised_price_for_asset_class_service
        )

    async def seed_calculate_risk_data_async(self):
        """
        Asynchronously seed the database of risk calculations using predefined schemas.
        """
        self.logger.info("Data processing for risk calculations has started")
        models = [
            # DailyReturnsVolModel,
            # InstrumentVolModel,
            # DailyVolNormalizedReturnsModel,
            DailyVolNormalisedPriceForAssetClassModel,
        ]
        for model in models:
            await self._get_risk_data_from_raw_file(model)

    async def _get_risk_data_from_raw_file(self, model):
        """
        Data processing for CSV files.
        """
        if model.__tablename__ == "daily_returns_volatility":
            await self.seed_daily_returns_vol_service.seed_daily_returns_vol_async()
        elif model.__tablename__ == "instrument_volatility":
            await self.seed_instrument_vol_service.seed_instrument_volatility_async()
        elif model.__tablename__ == "daily_vol_normalized_returns":
            await self.seed_daily_vol_normalised_returns_service.seed_daily_normalised_returns_vol_async()
        elif model.__tablename__ == "daily_vol_normalised_price_for_asset_class":
            await self.seed_daily_vol_normalised_price_for_asset_class_service.seed_daily_vol_normalised_price_for_asset_class_async()
        else:
            raise ValueError(f"Unrecognized table name: {model.__tablename__}")
