from fastapi import Depends, Request

from common.src.database.repository import Repository
from raw_data.src.models.config_models import InstrumentMetadataModel, RollConfigModel, SpreadCostsModel
from raw_data.src.models.instrument_config_models import InstrumentConfigModel
from raw_data.src.services.instrument_config_service import InstrumentConfigService


def get_instrument_config_repository(request: Request) -> Repository[InstrumentConfigModel]:
    return Repository(request.app.async_pool, InstrumentConfigModel)


def get_instrument_metadata_repository(request: Request) -> Repository[InstrumentMetadataModel]:
    return Repository(request.app.async_pool, InstrumentMetadataModel)


def get_roll_config_repository(request: Request) -> Repository[RollConfigModel]:
    return Repository(request.app.async_pool, RollConfigModel)


def get_spread_cost_repository(request: Request) -> Repository[SpreadCostsModel]:
    return Repository(request.app.async_pool, SpreadCostsModel)


def get_instrument_config_service(
    repository: Repository[InstrumentConfigModel] = Depends(get_instrument_config_repository),
) -> InstrumentConfigService:
    """
    Dependency injection method for InstrumentConfigService.
    """
    return InstrumentConfigService(repository=repository)
