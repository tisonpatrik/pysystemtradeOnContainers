from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import NormalisedPriceForAssetSeedError
from src.raw_data.models.config_models import InstrumentConfig
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.errors.normalised_price_for_asset_class_error import (
    NormalisedPriceForAssetClassCalculationError,
)
from src.risk.estimators.normalised_price_for_asset_class import (
    NormalisedPriceForAssetClass,
)
from src.risk.models.risk_models import DailyVolNormalisedPriceForAssetClass
from src.risk.services.cumulative_daily_vol_normalised_returns_service import (
    CumulativeDailyVolatilityNormalisedReturnsService,
)
from src.risk.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)


class NormalisedPriceForAssetClassService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.daily_vol_normalised_price_for_asset_class_service = (
            DailyVolNormalisedPriceForAssetClassService(db_session)
        )
        self.cumulative_daily_volatility_normalised_returns_service = (
            CumulativeDailyVolatilityNormalisedReturnsService(db_session)
        )
        self.normalised_price_for_asset_class = NormalisedPriceForAssetClass()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.daily_vol_normalised_price_for_asset_service = (
            DailyVolNormalisedPriceForAssetClassService(db_session)
        )

    async def get_normalised_price_for_asset_class_async(
        self, asset_class: str, symbol: str
    ):
        """Get normalised price for asset class."""
        try:
            normalised_price_for_asset_class = await self.daily_vol_normalised_price_for_asset_class_service.get_daily_vol_normalised_price_for_asset_class_async(
                asset_class
            )
            normalised_price_for_given_instrument = await self.cumulative_daily_volatility_normalised_returns_service.get_cumulative_vol_for_prices_async(
                symbol
            )
            normalised_price_for_asset_class_aligned = self.normalised_price_for_asset_class.get_normalised_price_for_asset_class(
                normalised_price_for_given_instrument,
                normalised_price_for_asset_class,
            )

            return normalised_price_for_asset_class_aligned

        except Exception as exc:
            self.logger.error(
                f"Error in calculating normalised price for asset class: {exc}"
            )
            raise NormalisedPriceForAssetClassCalculationError()

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
