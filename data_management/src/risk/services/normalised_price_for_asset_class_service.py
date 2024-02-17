from src.core.utils.logging import AppLogger
from src.risk.errors.normalised_price_for_asset_class_error import (
    NormalisedPriceForAssetClassCalculationError,
)
from src.risk.estimators.normalised_price_for_asset_class import (
    NormalisedPriceForAssetClass,
)
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
