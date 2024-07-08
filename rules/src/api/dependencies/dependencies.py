from fastapi import Depends

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository
from rules.src.api.handlers.rules_handler import RulesHandler


def get_rules_handler(repository: Repository = Depends(get_repository)) -> RulesHandler:
	return RulesHandler(repository=repository)
