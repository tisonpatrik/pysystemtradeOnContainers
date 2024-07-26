from rules_manager.src.validation.create_rule import CreateRule
from rules_manager.src.validation.delete_rule import DeleteRule

from common.src.cqrs.db_queries.get_all_rules import GetAllRules
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.rule import Rule


class RulesHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def create_rule_async(self, rule: Rule):
        try:
            statement = CreateRule(rule)
            await self.repository.insert_item_async(statement)
        except Exception as e:
            self.logger.error(f"Error creating rule, Error: {str(e)}")
            raise e

    async def get_all_rules_async(self):
        try:
            statement = GetAllRules()
            rules_data = await self.repository.fetch_many_async(statement)
            rules = [to_pydantic(rule_data, Rule) for rule_data in rules_data]
            return rules
        except Exception as e:
            self.logger.error(f"Error fetching all rules, Error: {str(e)}")
            raise e

    async def delete_rule_async(self, rule: Rule):
        try:
            statement = DeleteRule(rule)
            await self.repository.delete_item_async(statement)
        except Exception as e:
            self.logger.error(f"Error deleting rule, Error: {str(e)}")
            raise e
