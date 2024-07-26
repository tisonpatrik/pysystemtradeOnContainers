import asyncio

from celery import Celery

from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger

celery_app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

messages = [
    {"name": "tasks.breakout", "speed": 500000, "queue": "breakout"},
    {"name": "tasks.accel", "speed": 200000, "queue": "accel"},
    {"name": "tasks.breakout", "speed": 150000, "queue": "breakout"},
    {"name": "tasks.accel", "speed": 2, "queue": "accel"},
]


class RawForecastHandler:
    def __init__(self, db_repository: Repository):
        self.logger = AppLogger.get_instance().get_logger()
        self.db_repository = db_repository

    async def get_raw_forecast_async(self):
        self.logger.info("Fetching raw forecast")

        # Send all messages and gather results
        tasks = [self.send_celery_task_async(message["name"], message["speed"], message["queue"]) for message in messages]
        results = await asyncio.gather(*tasks)

        # Aggregate results
        aggregated_result = self.aggregate_results(results)
        return {"raw_forecast": aggregated_result}

    async def send_celery_task_async(self, task_name, speed, queue):
        loop = asyncio.get_event_loop()
        task = celery_app.send_task(task_name, args=[speed], queue=queue)
        result = await loop.run_in_executor(None, task.get, 5)
        return result

    def aggregate_results(self, results):
        # Placeholder for actual aggregation logic
        aggregated_result = {"total_results": sum(results)}
        return aggregated_result
