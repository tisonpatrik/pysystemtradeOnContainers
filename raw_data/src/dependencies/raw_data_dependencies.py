from fastapi import Depends

from common.src.database.repository import Repository
from raw_data.src.dependencies.raw_data_repositories import get_adjusted_prices_repository
from raw_data.src.models.raw_data_models import AdjustedPricesModel
from raw_data.src.services.adjusted_prices_service import AdjustedPricesService


def get_adjusted_prices_service(
    repository: Repository[AdjustedPricesModel] = Depends(get_adjusted_prices_repository),
) -> AdjustedPricesService:
    """
    Dependency injection method for AdjustedPricesService.
    """
    return AdjustedPricesService(repository=repository)
