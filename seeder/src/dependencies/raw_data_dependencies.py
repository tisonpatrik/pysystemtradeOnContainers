from fastapi import Depends
from src.services.raw_data.seed_adjusted_prices_service import SeedAdjustedPricesService
from src.services.raw_data.seed_fx_prices_service import SeedFxPricesService
from src.services.raw_data.seed_multiple_prices_service import SeedMultiplePricesService
from src.services.raw_data.seed_roll_calendars_service import SeedRollCalendarsService

from common.src.database.repository import Repository
from raw_data.src.dependencies.repositories import (
    get_adjusted_prices_repository,
    get_fx_prices_repository,
    get_multiple_prices_repository,
    get_roll_calendars_repository,
)


def get_seed_adjusted_prices_service(
    repository: Repository = Depends(get_adjusted_prices_repository),
) -> SeedAdjustedPricesService:
    return SeedAdjustedPricesService(repository)


def get_seed_fx_prices_service(repository: Repository = Depends(get_fx_prices_repository)) -> SeedFxPricesService:
    return SeedFxPricesService(repository)


def get_seed_multiple_prices_service(
    repository: Repository = Depends(get_multiple_prices_repository),
) -> SeedMultiplePricesService:
    return SeedMultiplePricesService(repository)


def get_seed_roll_calendars_service(
    repository: Repository = Depends(get_roll_calendars_repository),
) -> SeedRollCalendarsService:
    return SeedRollCalendarsService(repository)
