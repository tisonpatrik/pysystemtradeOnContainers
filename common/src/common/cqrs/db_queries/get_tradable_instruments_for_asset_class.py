from common.database.base_statements.fetch_statement import FetchStatement


class GetTradableInstrumentsForAssetClass(FetchStatement):
    def __init__(self, asset_class: str, is_tradable: bool):
        self._query = """
        SELECT symbol
        FROM instrument_config
        WHERE asset_class = $1 AND  is_tradable = $2
        ORDER BY symbol ASC;
        """
        self._parameters = (asset_class, is_tradable)

    @property
    def parameters(self) -> tuple:
        return self._parameters
