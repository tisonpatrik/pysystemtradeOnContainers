from common.src.cqrs.api_queries.get_rule_for_instrument import GetRuleForInstrumentQuery
from common.src.database.repository import Repository
from common.src.logging.logger import AppLogger
from rules.src.services.breakout import BreakoutService


class BreakoutHandler:
    def __init__(self, repository: Repository):
        self.accel_service = BreakoutService()
        self.repository = repository
        self.logger = AppLogger.get_instance().get_logger()

    async def get_breakout_async(self, request: GetRuleForInstrumentQuery):
        self.logger.info(f"Calculating Breakout rule for {request}")
