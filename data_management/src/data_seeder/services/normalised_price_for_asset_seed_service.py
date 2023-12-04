from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import NormalisedPriceForAssetSeedError
from src.raw_data.services.instrument_config_services import InstrumentConfig
from src.risk.models.risk_models import NormalisedPriceForAssetClass
from src.risk.services.daily_volatility_normalised_returns_service import (
    DailyVolatilityNormalisedReturnsService,
)


class NormalisedPriceForAssetSeedService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfig(db_session)
        self.volatility_returns_service = DailyVolatilityNormalisedReturnsService(
            db_session
        )

    async def seed_normalised_price_for_asset_class(self):
        """Calculates normalised prices for asset class."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                NormalisedPriceForAssetClass.__tablename__,
            )
            groups = (
                await self.instrument_config_service.get_groups_of_assets_by_symbols_async()
            )
            for group in groups.iter_rows(named=True):
                asset_class = group[groups.columns[0]]
                list_of_instruments = group[groups.columns[1]].split(", ")
                aggregate_returns_across_instruments_list = [
                    await self.volatility_returns_service.get_daily_vol_normalised_returns_async(
                        instrument_code
                    )
                    for instrument_code in list_of_instruments
                ]

        except NormalisedPriceForAssetSeedError as error:
            self.logger.error("An error occurred during seeding: %s", error)
            raise
