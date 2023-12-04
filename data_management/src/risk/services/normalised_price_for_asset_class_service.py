from src.core.utils.logging import AppLogger
from src.raw_data.services.instrument_config_services import InstrumentConfigService
from src.risk.errors.normalised_price_for_asset_class_error import (
    NormalisedPriceForAssetClassCalculationError,
)
from src.risk.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)


class NormalisedPriceForAssetClassService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.daily_vol_normalised_price_for_asset_class_service = (
            DailyVolNormalisedPriceForAssetClassService(db_session)
        )

    async def insert_normalised_price_for_asset_class_async(
        self, symbol, cumulative_normalised_price
    ):
        """Calculates and insert normalised price for asset class."""
        try:
            self.logger.info(
                "Starting the normalised price for asset class for %s symbol.",
                symbol,
            )
            asset_class = (
                await self.instrument_config_service.get_assets_class_by_symbol_async(
                    symbol
                )
            )
            normalised_price_for_asset_class = await self.daily_vol_normalised_price_for_asset_class_service.get_daily_vol_normalised_price_for_asset_class_async(
                asset_class
            )

        except Exception as exc:
            self.logger.error(
                f"Error in calculating normalised price for asset class: {exc}"
            )
            raise NormalisedPriceForAssetClassCalculationError()
