from src.models.config_models import InstrumentConfig

from common.src.database.entity_repository import EntityRepository
from common.src.logging.logger import AppLogger


class TestHandler:
    """
    This class provides methods to seed the database
    asynchronously from CSV files according to given schemas.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = EntityRepository(db_session, InstrumentConfig)

    async def get_config_items_count_async(self):
        """
        Asynchronously retrieves the count of configuration items from the database.
        """
        try:
            self.logger.info("Retrieving count of configuration items")
            items = await self.repository.get_all_async()
            count = len(items)
            self.logger.info(f"Retrieved count of config items: {count}")
            return count
        except Exception as e:
            self.logger.error(
                f"Error occurred while retrieving config items count: {str(e)}"
            )
            raise
