from common.database.base_statements.fetch_statement import FetchStatement


class GetAllInstrumentsForAssetClass(FetchStatement):
    def __init__(self, asset_class: str):
        self._query = """
        SELECT symbol
        FROM instrument_config
        WHERE asset_class = $1 AND have_data = true
        ORDER BY symbol ASC;
        """
        self._parameters = (asset_class,)

    @property
    def parameters(self) -> tuple:
        return self._parameters
