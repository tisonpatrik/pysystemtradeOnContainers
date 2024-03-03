from src.app.models.risk_models import DailyVolNormalisedPriceForAssetClass
from src.estimators.normalised_price_for_asset_class import NormalisedPriceForAssetClass
from src.services.raw_data.instrument_config_services import InstrumentConfigService
from src.services.risk.cumulative_daily_vol_normalised_returns_service import (
    CumulativeDailyVolatilityNormalisedReturnsService,
)
from src.services.risk.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)

from common.logging.logger import AppLogger


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
            error_message = f"Error in calculating normalised price for asset class '{asset_class}' with symbol '{symbol}': {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)

    async def seed_normalised_price_for_asset_class_async(self):
        """Calculates normalised prices for asset class."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                DailyVolNormalisedPriceForAssetClass.__tablename__,
            )
            assets = await self.instrument_config_service.get_assets_async()
            for asset_class in assets:
                await self.daily_vol_normalised_price_for_asset_service.insert_daily_vol_normalised_price_for_asset_class_async(
                    asset_class=asset_class
                )

        except Exception as exc:
            error_message = f"An error occurred during seeding: {exc}"
            self.logger.error(error_message)
            raise ValueError(error_message)
