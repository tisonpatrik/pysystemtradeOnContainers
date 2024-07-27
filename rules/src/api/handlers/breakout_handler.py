from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.logging.logger import AppLogger
from rules.src.services.accel import AccelService


class BreakoutHandler:
    def __init__(self, repository: Repository, client: RestClient):
        self.logger = AppLogger.get_instance().get_logger()
        self.accel_service = AccelService()
        self.repository = repository
        self.client = client

    async def get_breakout_async(self, request: GetRuleForInstrumentQuery):
        self.logger.info(f"Calculating Breakout rule for {request}")
