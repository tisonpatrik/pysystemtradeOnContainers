from common.src.commands.db_commands.create_rule import CreateRule
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.queries.api_queries.get_rule import GetRuleQuery
from common.src.queries.db_queries.get_rule import GetRule
from common.src.utils.convertors import to_pydantic
from common.src.validation.rule import Rule


class RulesHandler:
	def __init__(self, repository: Repository) -> None:
		self.logger = AppLogger.get_instance().get_logger()
		self.repository = repository

	async def get_rule_async(self, get_rule_query: GetRuleQuery):
		try:
			statement = GetRule(get_rule_query.name, get_rule_query.speed)
			rule_data = await self.repository.fetch_item_async(statement)
			rule = to_pydantic(rule_data, Rule)
			if rule is None:
				raise ValueError(f'No data found for rule {get_rule_query.name} with speed {get_rule_query.speed}')
			return rule

		except Exception as e:
			self.logger.error(f'Error fetching all rules, Error: {str(e)}')
			raise e

	async def create_rule_async(self, rule: Rule):
		try:
			statement = CreateRule(rule)
			await self.repository.insert_object_async(statement)
		except Exception as e:
			self.logger.error(f'Error creating rule, Error: {str(e)}')
			raise e
