from src.core.utils.logging import AppLogger
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.errors.daily_returns_vol_processing_error import (
    DailyReturnsVolProcessingError,
    DailyReturnsVolProcessingHaltedError,
)
from src.risk.estimators.daily_returns import daily_returns_volatility


class DailyReturnsVolatilityCalculator:
    """
    Class for calculating daily returns volatility of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_service = AdjustedPricesService(db_session)

    async def get_daily_returns_vols_async(self, instrument_configs, model):
        processed_vols = []
        for config in instrument_configs.to_dict(orient='records'):
            try:
                volatility = await self.process_daily_returns_vol_async(config, model)
                processed_vols.append(volatility)
            except DailyReturnsVolProcessingError as exc:
                self.logger.error(
                    f"Error processing volatility for config {config}: {exc}"
                )
                raise DailyReturnsVolProcessingHaltedError()
        return processed_vols

    async def process_daily_returns_vol_async(self, config, model):
        """
        Process and calculate the volatility for a given instrument configuration.
        """
        try:
            symbol = config[model.symbol.key]

            # Fetching daily and multiple prices
            daily_prices = await self.adjusted_prices_service.get_daily_prices_async(
                symbol
            )
            # Calculate volatility
            volatility = daily_returns_volatility(daily_prices)
            return volatility

        except KeyError as exc:
            self.logger.error(f"Key error in configuration: {exc}")
            raise DailyReturnsVolProcessingHaltedError()

        except Exception as exc:
            self.logger.error(
                f"General error processing daily returns volatility: {exc}"
            )
            raise DailyReturnsVolProcessingHaltedError()
