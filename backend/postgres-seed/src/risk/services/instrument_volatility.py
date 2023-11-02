import logging
import pandas as pd

from src.risk.schemas.instrument_volatility_schema import InstrumentVolatilitySchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstrumentVolatilityService:
    def __init__(self):
        self.risk_schema = InstrumentVolatilitySchema()

    def calculate_instrument_volatility_for_instrument(
        self, series: pd.Series, symbol: str
    ) -> pd.DataFrame:
        try:
            volatility = robust_vol_calc(series).dropna()
            data_frame = pd.DataFrame(volatility)
            data_frame.reset_index(inplace=True)
            renamed = rename_columns(data_frame, self.risk_schema.columns)
            unix_timed = convert_datetime_to_unixtime(
                renamed, self.risk_schema.index_column
            )
            populated = add_column_and_populate_it_by_value(
                unix_timed, "symbol", symbol
            )
            return populated
        except Exception as error:
            logger.error(
                "Failed to calculate volatility for instrument %s: %s",
                symbol,
                error,
                exc_info=True,
            )
            raise
