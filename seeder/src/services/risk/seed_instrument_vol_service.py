from common.src.logging.logger import AppLogger


class SeedInstrumentVolService:
    def __init__(self):
        self.logger = AppLogger.get_instance().get_logger()

    async def seed_instrument_volatility_async(self):
        """
        Seed the database with instrument volatility data.
        """
        self.logger.info("Seeding instrument volatility data")
