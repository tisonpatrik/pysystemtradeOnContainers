from fastapi import Depends, Request

from common.src.database.repository import Repository
from common.src.dependencies.database_dependencies import get_db
from raw_data.src.models.config_models import InstrumentMetadataModel, RollConfigModel, SpreadCostsModel
from raw_data.src.models.instrument_config_models import InstrumentConfigModel
from raw_data.src.services.instrument_config_service import InstrumentConfigService


def get_instrument_config_repository(request: Request = Depends(get_db)) -> Repository[InstrumentConfigModel]:
    return Repository(request, InstrumentConfigModel)


def get_instrument_metadata_repository(request: Request = Depends(get_db)) -> Repository[InstrumentMetadataModel]:
    return Repository(request, InstrumentMetadataModel)


def get_roll_config_repository(request: Request = Depends(get_db)) -> Repository[RollConfigModel]:
    return Repository(request, RollConfigModel)


def get_spread_cost_repository(request: Request = Depends(get_db)) -> Repository[SpreadCostsModel]:
    return Repository(request, SpreadCostsModel)


def get_instrument_config_service(
    repository: Repository[InstrumentConfigModel] = Depends(get_instrument_config_repository),
) -> InstrumentConfigService:
    """
    Dependency injection method for InstrumentConfigService.
    """
    return InstrumentConfigService(repository=repository)
