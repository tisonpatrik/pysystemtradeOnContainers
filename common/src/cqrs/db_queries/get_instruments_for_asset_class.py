from common.src.database.base_statements.fetch_statement import FetchStatement


class GetInstrumentsForAssetClass(FetchStatement):
    def __init__(self, symbol: str):
        self._query = """
        SELECT symbol
        FROM instrument_config
        WHERE asset_class = $1
        ORDER BY symbol ASC;
        """
        self._parameters = (symbol,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
