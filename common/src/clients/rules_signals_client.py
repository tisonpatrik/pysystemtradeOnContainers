import pandas as pd

from common.src.cqrs.db_queries.get_all_rules import GetAllRules
from common.src.database.repository import Repository
from common.src.http_client.rest_client import RestClient
from common.src.utils.convertors import to_pydantic
from common.src.utils.rule_query_factory import RuleQueryFactory
from common.src.validation.rule import Rule
from common.src.validation.rule_signal import RuleSignal
from common.src.validation.scaling_type import ScalingType


class RulesSignalsClient:
    def __init__(self, db_repository: Repository, rest_client: RestClient):
        self.repository = db_repository
        self.client = rest_client

    async def get_trading_rule_list_async(self, symbol: str) -> list:
        statement = GetAllRules()
        instruments_data = await self.repository.fetch_many_async(statement)
        if instruments_data is None:
            raise ValueError("No data found for instruments ")
        return [to_pydantic(instrument, Rule) for instrument in instruments_data]

    async def get_forecast_by_rule_async(self, symbol: str, rule: Rule) -> pd.Series:
        rule_query_factory = RuleQueryFactory(ScalingType.FIXED)
        query = rule_query_factory.create_rule_query(symbol, rule)
        rule_signal_data = await self.client.get_data_async(query)
        return RuleSignal.from_api_to_series(rule_signal_data)

    async def get_forecast_weights_async(self, symbol: str) -> pd.DataFrame:
        return pd.DataFrame()

    async def get_estimated_scaling_factor_async(self) -> pd.Series:
        return pd.Series()
