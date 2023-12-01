from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import NormalisedPriceForAssetSeedError
from src.raw_data.services.instrument_metadata_service import InstrumentMetadataService
from src.risk.models.risk_models import NormalisedPriceForAssetClass


class NormalisedPriceForAssetSeedService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_service = InstrumentMetadataService(db_session)

    async def seed_normalised_price_for_asset_class(self):
        """Calculates normalised prices for asset class."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                NormalisedPriceForAssetClass.__tablename__,
            )

        except NormalisedPriceForAssetSeedError as error:
            self.logger.error("An error occurred during seeding: %s", error)
            raise
