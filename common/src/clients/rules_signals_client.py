import pandas as pd

from common.src.database.repository import Repository


class RulesSignalsClient:
    def __init__(self, db_repository: Repository):
        self.db_repository = db_repository

    async def get_estimated_scaling_factor_async(self) -> pd.Series:
        return pd.Series()
