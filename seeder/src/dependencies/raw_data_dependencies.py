from fastapi import Depends, Request
from src.services.raw_data.seed_adjusted_prices_service import SeedAdjustedPricesService
from src.services.raw_data.seed_fx_prices_service import SeedFxPricesService
from src.services.raw_data.seed_multiple_prices_service import SeedMultiplePricesService
from src.services.raw_data.seed_roll_calendars_service import SeedRollCalendarsService

from common.src.database.repository import Repository


def get_repository(request: Request) -> Repository:
    return Repository(request.app.async_pool)


def get_seed_adjusted_prices_service(
    repository: Repository = Depends(get_repository),
) -> SeedAdjustedPricesService:
    return SeedAdjustedPricesService(repository)


def get_seed_fx_prices_service(repository: Repository = Depends(get_repository)) -> SeedFxPricesService:
    return SeedFxPricesService(repository)


def get_seed_multiple_prices_service(
    repository: Repository = Depends(get_repository),
) -> SeedMultiplePricesService:
    return SeedMultiplePricesService(repository)


def get_seed_roll_calendars_service(
    repository: Repository = Depends(get_repository),
) -> SeedRollCalendarsService:
    return SeedRollCalendarsService(repository)
