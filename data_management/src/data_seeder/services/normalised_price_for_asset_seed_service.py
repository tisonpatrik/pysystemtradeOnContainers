from src.core.utils.logging import AppLogger
from src.data_seeder.errors.risk_seeding_errors import NormalisedPriceForAssetSeedError
from src.raw_data.services.instrument_metadata_service import InstrumentMetadataService
from src.risk.models.risk_models import NormalisedPriceForAssetClass


class NormalisedPriceForAssetSeedService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_metadata_service = InstrumentMetadataService(db_session)

    async def seed_normalised_price_for_asset_class(self):
        """Calculates normalised prices for asset class."""
        try:
            self.logger.info(
                "Starting the process for %s table.",
                NormalisedPriceForAssetClass.__tablename__,
            )
            groups = (
                await self.instrument_metadata_service.get_groups_of_assets_by_symbols_async()
            )
            for group in groups.iter_rows(named=True):
                asset_class = group[groups.columns[0]]
                instruments = group[groups.columns[1]].split(", ")
                

        except NormalisedPriceForAssetSeedError as error:
            self.logger.error("An error occurred during seeding: %s", error)
            raise
