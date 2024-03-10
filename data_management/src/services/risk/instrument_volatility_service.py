from risk.src.models.risk_models import InstrumentVolatility
from src.app.schemas.risk_schemas import InstrumentVolatilitySchema
from src.core.pandas.prapare_db_calculations import prepara_data_to_db
from src.estimators.instrument_volatility import InstrumentVolEstimator
from src.services.raw_data.instrument_config_services import InstrumentConfigService
from src.services.raw_data.multiple_prices_service import MultiplePricesService

from common.src.logging.logger import AppLogger

table_name = InstrumentVolatility.__tablename__


class InstrumentVolatilityService:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.instrument_config_service = InstrumentConfigService(db_session)
        self.multiple_prices_service = MultiplePricesService(db_session)
        self.instrument_vol_estimator = InstrumentVolEstimator()

    async def insert_instrument_vol_for_prices_async(
        self, multiple_prices, point_size, daily_returns_vol, symbol
    ):
        """Calculates and insert instrument volatility of a given prices."""
        try:
            self.logger.info(
                "Starting the instrument volatility calculation for %s symbol.",
                symbol,
            )

            instrument_vols = self.instrument_vol_estimator.get_instrument_currency_vol(
                multiple_prices=multiple_prices,
                daily_returns_vol=daily_returns_vol,
                point_size=point_size,
            )
            prepared_data = prepara_data_to_db(
                instrument_vols, InstrumentVolatility, symbol
            )
            # await self.repository.insert_data_async(
            #     prepared_data, InstrumentVolatilitySchema
            # )
            print("neco")
        except Exception as exc:
            error_message = (
                f"Error in calculating instrument volatility for {symbol}: {exc}"
            )
            self.logger.error(error_message)
            raise ValueError(error_message)
