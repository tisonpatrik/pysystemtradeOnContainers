from common.src.cqrs.api_queries.get_forecast_for_symbol_query import GetForecastForSymbolQuery
from common.src.cqrs.db_queries.get_all_rules import GetAllRules
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.rule import Rule




class RawForecastHandler:
    def __init__(self, db_repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = db_repository

    async def get_raw_forecast_async(self, forecast_query: GetForecastForSymbolQuery):
        self.logger.info("Fetching raw forecast")
        rules = await self._get_all_rules_async()
        self.logger.info(f"Fetched rules: {rules}")
        # Send all messages and gather results


    async def _get_all_rules_async(self):
        try:
            statement = GetAllRules()
            rules_data = await self.repository.fetch_many_async(statement)
            rules = [to_pydantic(rule_data, Rule) for rule_data in rules_data]
            return rules
        except Exception as e:
            self.logger.error(f"Error fetching all rules, Error: {str(e)}")
            raise e
