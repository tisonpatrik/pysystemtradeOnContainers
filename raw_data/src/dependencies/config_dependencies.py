from fastapi import Depends

from common.src.database.repository import Repository
from raw_data.src.dependencies.config_repositories import get_instrument_config_repository
from raw_data.src.models.instrument_config_models import InstrumentConfigModel
from raw_data.src.services.instrument_config_service import InstrumentConfigService


def get_instrument_config_service(
    repository: Repository[InstrumentConfigModel] = Depends(get_instrument_config_repository),
) -> InstrumentConfigService:
    """
    Dependency injection method for InstrumentConfigService.
    """
    return InstrumentConfigService(repository=repository)
