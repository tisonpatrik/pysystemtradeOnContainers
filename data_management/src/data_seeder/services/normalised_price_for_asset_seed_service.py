from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import NormalisedPriceForAssetSeedError
from src.raw_data.models.config_models import InstrumentConfig
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.models.risk_models import DailyVolNormalisedPriceForAssetClass
from src.risk.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)


class NormalisedPriceForAssetSeedService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.daily_vol_normalised_price_for_asset_service = (
            DailyVolNormalisedPriceForAssetClassService(db_session)
        )

    async def seed_normalised_price_for_asset_class_async(self):
        """Calculates normalised prices for asset class."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyVolNormalisedPriceForAssetClass.__tablename__,
            )
            assets = await self.instrument_config_service.get_unique_values_for_given_column_from_instrumnet_config(
                InstrumentConfig.asset_class.key
            )
            for asset_class in assets:
                await self.daily_vol_normalised_price_for_asset_service.insert_daily_vol_normalised_price_for_asset_class_async(
                    asset_class=asset_class
                )

        except NormalisedPriceForAssetSeedError as error:
            self.logger.error("An error occurred during seeding: %s", error)
            raise
