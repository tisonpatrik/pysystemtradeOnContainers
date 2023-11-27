from src.core.utils.logging import AppLogger
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.errors.daily_returns_vol_processing_error import (
    DailyReturnsVolProcessingError,
    DailyReturnsVolProcessingHaltedError,
)
from src.risk.estimators.daily_returns import daily_returns_volatility
from src.core.data_types_conversion.to_frame import convert_series_to_frame
from src.raw_data.utils.add_and_populate_column import add_column_and_populate_it_by_value
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
                symbol = config[model.symbol.key]
                volatility = await self.process_daily_returns_vol_async(symbol)
                framed = convert_series_to_frame(volatility)
                populated = add_column_and_populate_it_by_value(framed,model.symbol.key, symbol)
                processed_vols.append(populated)
            except DailyReturnsVolProcessingError as exc:
                self.logger.error(
                    f"Error processing volatility for config {config}: {exc}"
                )
                raise DailyReturnsVolProcessingHaltedError()
        return processed_vols

    async def process_daily_returns_vol_async(self, symbol):
        """
        Process and calculate the volatility for a given instrument configuration.
        """
        try:
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
