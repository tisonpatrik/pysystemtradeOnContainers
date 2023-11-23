from src.core.errors.seeder_error import DataInsertionError
from src.core.utils.logging import AppLogger
from src.db.services.data_insert_service import DataInsertService
from src.risk.models.risk_models import InstrumentVolatility, RobustVolatility
from src.risk.services.instrument_volatility_service import InstrumentVolatilityService
from src.risk.services.robust_volatility_service import RobustVolatilityService


class RiskHandler:
    def __init__(self, db_session):
        self.logger = AppLogger.get_instance().get_logger()
        self.data_insert_service = DataInsertService(db_session)
        self.robust_volatility_service = RobustVolatilityService(db_session)
        self.instrument_volatility_service = InstrumentVolatilityService(db_session)

    async def calculate_risk_data_async(self):
        """
        Asynchronously seed the database of risk calculations using predefined schemas.
        """
        self.logger.info("Data processing for risk calculations has started")
        models = [
            # RobustVolatility,
            InstrumentVolatility
        ]

        for model in models:
            try:
                data = await self._get_risk_data_from_raw_file(model)
                # await self.data_insert_service.async_insert_dataframe_to_table(data, model.__tablename__)
            except DataInsertionError as error:
                self.logger.error(
                    f"Data insertion failed for {model.__tablename__}: {error}"
                )
                raise error

    async def _get_risk_data_from_raw_file(self, model):
        """
        Data processing for CSV files.
        """
        if model.__tablename__ in "robust_volatility":
            return await self.robust_volatility_service.calculate_robust_volatility_for_instrument_async(
                model
            )
        if model.__tablename__ in "instrument_volatility":
            return await self.instrument_volatility_service.calculate_instrument_volatility_for_instrument_async(
                model
            )
        raise ValueError(f"Unrecognized table name: {model.__tablename__}")
