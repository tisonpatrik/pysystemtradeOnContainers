from pandera.errors import SchemaError

from common.src.logging.logger import AppLogger
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from risk.src.models.risk_models import DailyVolNormalisedPriceForAssetClassModel
from risk.src.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)
from risk.src.services.daily_vol_normalised_returns_service import DailyVolatilityNormalisedReturnsService


class SeedDailyVolNormalisedPriceForAssetClassService:
    """Service for seeding daily volatility normalized price fpr asset class of financial instruments."""

    def __init__(
        self,
        instrument_config_service: InstrumentConfigService,
        daily_vol_normalised_price_for_asset_class_service: DailyVolNormalisedPriceForAssetClassService,
        daily_vol_normalised_returns_service: DailyVolatilityNormalisedReturnsService,
        prices_service: AdjustedPricesService,
    ):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = instrument_config_service
        self.daily_vol_normalised_price_for_asset_class_service = daily_vol_normalised_price_for_asset_class_service
        self.daily_vol_normalised_returns_service = daily_vol_normalised_returns_service
        self.prices_service = prices_service

    async def seed_daily_vol_normalised_price_for_asset_class_async(self):
        """Seed daily volatility normalised price for asset class."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyVolNormalisedPriceForAssetClassModel.__tablename__,
            )
            assets = await self.instrument_config_service.get_asset_classes_async()
            for asset in assets:
                aggregate_returns_across_instruments_list = await self.daily_vol_normalised_returns_service.get_daily_vol_normalised_returns_for_instruments_async(
                    asset.asset_class
                )
                vol_normalised_price = self.daily_vol_normalised_price_for_asset_class_service.calculate_daily_vol_normalised_price_for_asset_class_async(
                    aggregate_returns_across_instruments_list
                )
                await self.daily_vol_normalised_price_for_asset_class_service.insert_daily_vol_normalised_price_for_asset_class_async(
                    vol_normalised_price, asset.asset_class
                )

            self.logger.info(
                f"Successfully inserted {DailyVolNormalisedPriceForAssetClassModel.__name__} calculations for {len(assets)} assets."
            )
        except SchemaError as schema_exc:
            self.logger.error(f"Schema validation error: {schema_exc.failure_cases}")
            raise

        except Exception as e:
            self.logger.error("An unexpected error occurred during the seeding process: %s", str(e))
            raise
