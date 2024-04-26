from fastapi import Depends
from src.services.risk.seed_daily_returns_vol_service import SeedDailyReturnsVolService
from src.services.risk.seed_daily_vol_normalised_price_for_asset_class_service import (
    SeedDailyVolNormalisedPriceForAssetClassService,
)
from src.services.risk.seed_daily_vol_normalised_returns_service import SeedDailyVolNormalisedReturnsService
from src.services.risk.seed_instrument_vol_service import SeedInstrumentVolService

from raw_data.src.dependencies.dependencies import (
    get_adjusted_prices_service,
    get_instrument_config_service,
    get_multiple_prices_service,
)
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService
from raw_data.src.services.instrument_config_service import InstrumentConfigService
from raw_data.src.services.multiple_prices_service import MultiplePricesService
from risk.src.dependencies.risk_dependencies import (
    get_daily_returns_vol_service,
    get_daily_vol_normalised_price_for_asset_class_service,
    get_daily_vol_normalised_returns_service,
    get_instrument_vol_service,
)
from risk.src.services.daily_returns_vol_service import DailyReturnsVolService
from risk.src.services.daily_vol_normalised_price_for_asset_class_service import (
    DailyVolNormalisedPriceForAssetClassService,
)
from risk.src.services.daily_vol_normalised_returns_service import DailyVolatilityNormalisedReturnsService
from risk.src.services.instrument_currency_vol_service import InstrumentCurrencyVolService


def get_seed_daily_returns_vol_service(
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


def get_seed_instrument_vol_service(
    daily_returns_vol_service: DailyReturnsVolService = Depends(get_daily_returns_vol_service),
    instrument_config_service: InstrumentConfigService = Depends(get_instrument_config_service),
    multiple_prices_service: MultiplePricesService = Depends(get_multiple_prices_service),
    instrument_vol_service: InstrumentCurrencyVolService = Depends(get_instrument_vol_service),
) -> SeedInstrumentVolService:
    """
    Dependency injection method for InstrumentVolSeedService.
    """
    return SeedInstrumentVolService(
        daily_returns_vol_service=daily_returns_vol_service,
        instrument_config_service=instrument_config_service,
        multiple_prices_service=multiple_prices_service,
        instrument_vol_service=instrument_vol_service,
    )


def get_seed_daily_vol_normalised_returns_service(
    prices_service: AdjustedPricesService = Depends(get_adjusted_prices_service),
    daily_vol_normalised_returns_service: DailyVolatilityNormalisedReturnsService = Depends(
        get_daily_vol_normalised_returns_service
    ),
    instrument_config_service: InstrumentConfigService = Depends(get_instrument_config_service),
) -> SeedDailyVolNormalisedReturnsService:
    """
    Dependency injection method for SeedDailyVolNormalisedReturnsService.
    """
    return SeedDailyVolNormalisedReturnsService(
        prices_service=prices_service,
        daily_vol_normalised_returns_service=daily_vol_normalised_returns_service,
        instrument_config_service=instrument_config_service,
    )


def get_seed_daily_vol_normalised_price_for_asset_class_service(
    instrument_config_service: InstrumentConfigService = Depends(get_instrument_config_service),
    daily_vol_normalised_price_for_asset_class_service: DailyVolNormalisedPriceForAssetClassService = Depends(
        get_daily_vol_normalised_price_for_asset_class_service
    ),
    daily_vol_normalised_returns_service: DailyVolatilityNormalisedReturnsService = Depends(
        get_daily_vol_normalised_returns_service
    ),
    prices_service: AdjustedPricesService = Depends(get_adjusted_prices_service),
) -> SeedDailyVolNormalisedPriceForAssetClassService:
    """
    Dependency injection method for SeedDailyVolNormalisedPriceForAssetClassService.
    """
    return SeedDailyVolNormalisedPriceForAssetClassService(
        instrument_config_service=instrument_config_service,
        daily_vol_normalised_price_for_asset_class_service=daily_vol_normalised_price_for_asset_class_service,
        daily_vol_normalised_returns_service=daily_vol_normalised_returns_service,
        prices_service=prices_service,
    )
