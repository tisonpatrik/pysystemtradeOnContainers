from fastapi import Depends
from src.services.risk.seed_daily_returns_vol_service import SeedDailyReturnsVolService

from raw_data.src.dependencies.config_dependencies import get_instrument_config_service
from raw_data.src.dependencies.raw_data_dependencies import get_adjusted_prices_service
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from risk.src.dependencies.risk_dependencies import get_daily_returns_vol_service
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService


def get_daily_returns_vol_seed_service(
    prices_service: AdjustedPricesService = Depends(get_adjusted_prices_service),
    daily_returns_vol_service: DailyReturnsVolService = Depends(get_daily_returns_vol_service),
    instrument_config_service: InstrumentConfigService = Depends(get_instrument_config_service),
) -> SeedDailyReturnsVolService:
    """
    Dependency injection method for DailyReturnsVolSeedService.
    """
    return SeedDailyReturnsVolService(
        prices_service=prices_service,
        daily_returns_vol_service=daily_returns_vol_service,
        instrument_config_service=instrument_config_service,
    )
