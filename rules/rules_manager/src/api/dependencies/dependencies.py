from fastapi import Depends
from rules_manager.src.api.handlers.rules_handler import RulesHandler

from common.src.database.repository import Repository
from common.src.dependencies.core_dependencies import get_repository


def get_rules_handler(repository: Repository = Depends(get_repository)) -> RulesHandler:
	return RulesHandler(repository=repository)
