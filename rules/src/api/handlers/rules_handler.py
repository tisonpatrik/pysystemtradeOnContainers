from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.queries.api_queries.get_rules import GetRuleQuery


class RulesHandler:
	def __init__(self, repository: Repository) -> None:
		self.logger = AppLogger.get_instance().get_logger()
		self.repository = repository

	async def get_rule_async(self, get_rule_query: GetRuleQuery):
		try:
			pass

		except Exception as e:
			self.logger.error(f'Error fetching all rules, Error: {str(e)}')
			raise e
