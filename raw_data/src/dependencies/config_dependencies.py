from fastapi import Depends

from common.src.database.repository import Repository
from common.src.database.statement_factory import StatementFactory
from raw_data.src.dependencies.config_repositories import (
    get_instrument_config_repository,
    get_instrument_config_statement_factory,
)
from raw_data.src.models.instrument_config_models import InstrumentConfigModel
from raw_data.src.services.instrument_config_service import InstrumentConfigService


def get_instrument_config_service(
    repository: Repository[InstrumentConfigModel] = Depends(get_instrument_config_repository),
    statement_factory: StatementFactory = Depends(get_instrument_config_statement_factory),
) -> InstrumentConfigService:
    """
    Dependency injection method for InstrumentConfigService.
    """
    return InstrumentConfigService(repository=repository, statement_factory=statement_factory)
