from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from raw_data.src.api.handlers.fx_prices_handler import FxPricesHandler
from raw_data.src.dependencies.config_dependencies import get_instrument_config_repository
from raw_data.src.dependencies.raw_data_dependencies import get_fx_prices_repository
from raw_data.src.models.instrument_config_models import Instrument, InstrumentConfigModel
from raw_data.src.models.raw_data_models import FxPricesModel

router = APIRouter()
logger = AppLogger.get_instance().get_logger()


class FxRateResponse(BaseModel):
    symbol: str


@router.get(
    "/fx_prices_route/{symbol}/",
    status_code=status.HTTP_200_OK,
    name="Get Config Data",
)
async def get_fx_rate_by_symbol(
    symbol: str,
    fx_prices_repository: Repository[FxPricesModel] = Depends(get_fx_prices_repository),
    instrument_config_repository: Repository[InstrumentConfigModel] = Depends(get_instrument_config_repository),
):
    try:
        logger.info(f"Fetching FX rate for symbol: {symbol}")
        fx_prices_handler = FxPricesHandler(fx_prices_repository, instrument_config_repository)
        fx_rate = await fx_prices_handler.get_fx_prices_for_symbol_async(Instrument(symbol=symbol))

        if fx_rate is None:
            logger.error(f"FX rate not found for symbol: {symbol}")
            raise HTTPException(status_code=404, detail="FX rate not found")

        response = FxRateResponse(symbol=symbol)
        logger.info(f"Successfully fetched FX rate for symbol: {symbol}")
        return response
    except Exception as e:
        logger.error(f"Error fetching FX rate for symbol: {symbol}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
