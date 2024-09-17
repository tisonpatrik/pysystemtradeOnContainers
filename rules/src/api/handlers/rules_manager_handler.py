from common.src.cqrs.db_queries.get_all_rules import GetAllRules
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.rule import Rule
from rules.src.validation.create_rule import CreateRule


class RulesManagerHandler:
    def __init__(self, repository: Repository) -> None:
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = repository

    async def create_rule_async(self, rule: Rule):
        try:
            statement = CreateRule(rule)
            await self.repository.insert_item_async(statement)
        except Exception:
            self.logger.exception("Error creating rule")
            raise

    async def get_all_rules_async(self):
        try:
            statement = GetAllRules()
            rules_data = await self.repository.fetch_many_async(statement)
            return [to_pydantic(rule_data, Rule) for rule_data in rules_data]
        except Exception:
            self.logger.exception("Error fetching all rules")
            raise
