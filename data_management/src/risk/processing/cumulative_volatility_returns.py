from src.core.utils.logging import AppLogger
from src.raw_data.services.adjusted_prices_service import AdjustedPricesService
from src.risk.errors.cumulative_volatility_returns_errors import (
    CumulativeVolatilityReturnsProcessingError,
    CumulativeVolatilityReturnsProcessingHaltedError,
)
from src.risk.estimators.cumulative_daily_vol_normalised_returns import (
    get_cumulative_daily_vol_normalised_returns,
)


class CumulativeVolatilityReturnsCalculator:
    """
    Class for calculating cumulative volatility returns of financial instruments.
    """

    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.adjusted_prices_service = AdjustedPricesService(db_session)

    async def get_cumulative_volatilities_async(self, instrument_configs, model):
        cumulative_vols = []
        for config in instrument_configs.to_dicts():
            try:
                cumulative_volatility = (
                    await self.process_cumulative_volatility_return_async(config, model)
                )
                cumulative_vols.append(cumulative_volatility)
            except CumulativeVolatilityReturnsProcessingError as exc:
                self.logger.error(
                    f"Error processing cumulative volatility for config {config}: {exc}"
                )
                raise CumulativeVolatilityReturnsProcessingHaltedError()
        return cumulative_vols

    async def process_cumulative_volatility_return_async(self, config, model):
        """
        Process and calculate the cumulative volatility return for a given instrument configuration.
        """
        try:
            symbol = config[model.symbol.key]

            # Fetching daily prices
            daily_prices = await self.adjusted_prices_service.get_daily_prices_async(
                symbol
            )

            # Calculate cumulative volatility returns
            cumulative_volatility = get_cumulative_daily_vol_normalised_returns(
                daily_prices
            )
            return cumulative_volatility

        except KeyError as exc:
            self.logger.error(f"Key error in configuration: {exc}")
            raise CumulativeVolatilityReturnsProcessingHaltedError()

        except Exception as exc:
            self.logger.error(
                f"General error processing cumulative volatility returns: {exc}"
            )
            raise CumulativeVolatilityReturnsProcessingHaltedError()
