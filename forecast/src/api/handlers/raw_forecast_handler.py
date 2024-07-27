import asyncio

from celery import Celery

from common.src.cqrs.api_queries.get_forecast_for_symbol_query import GetForecastForSymbolQuery
from common.src.cqrs.db_queries.get_all_rules import GetAllRules
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from common.src.utils.convertors import to_pydantic
from common.src.validation.rule import Rule

celery_app = Celery("rules", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

messages = [
    {"name": "rules.breakout", "speed": 500000, "queue": "breakout"},
    {"name": "rules.accel", "speed": 200000, "queue": "accel"},
    {"name": "rules.breakout", "speed": 150000, "queue": "breakout"},
    {"name": "rules.accel", "speed": 2, "queue": "accel"},
]


class RawForecastHandler:
    def __init__(self, db_repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.repository = db_repository

    async def get_raw_forecast_async(self, forecast_query: GetForecastForSymbolQuery):
        self.logger.info("Fetching raw forecast")
        rules = await self._get_all_rules_async()
        self.logger.info(f"Fetched rules: {rules}")
        # Send all messages and gather results
        tasks = [self.send_celery_task_async(task_name=rule.task, speed=rule.speed, queue=rule.name) for rule in rules]
        results = await asyncio.gather(*tasks)

        # Aggregate results
        aggregated_result = self.aggregate_results(results)
        return {"raw_forecast": aggregated_result}

    async def send_celery_task_async(self, task_name: str, speed: int, queue: str):
        loop = asyncio.get_event_loop()
        task = celery_app.send_task(task_name, args=[speed], queue=queue)
        result = await loop.run_in_executor(None, task.get, 5)
        return result

    def aggregate_results(self, results):
        # Placeholder for actual aggregation logic
        aggregated_result = {"total_results": sum(results)}
        return aggregated_result

    async def _get_all_rules_async(self):
        try:
            statement = GetAllRules()
            rules_data = await self.repository.fetch_many_async(statement)
            rules = [to_pydantic(rule_data, Rule) for rule_data in rules_data]
            return rules
        except Exception as e:
            self.logger.error(f"Error fetching all rules, Error: {str(e)}")
            raise e
