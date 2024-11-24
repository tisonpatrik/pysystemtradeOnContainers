import pandas as pd

from common.cqrs.db_queries.get_carry_data import GetCarryDataQuery
from common.database.repository import PostgresClient
from common.validation.carry_data import CarryData


class CarryClient:
    def __init__(self, postgres: PostgresClient):
        self.postgres = postgres

    async def get_carry_data_async(self, symbol: str) -> pd.DataFrame:
        statement = GetCarryDataQuery(symbol=symbol)
        carry_data = await self.postgres.fetch_many_async(statement)
        return CarryData.from_db_to_dataframe(carry_data)
