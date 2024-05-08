from common.src.queries.base_statements.fetch_statement import FetchStatement
from common.src.validation.instrument_currency import InstrumentCurrency


class GetFxPrices(FetchStatement):
	def __init__(self, fx_code: str):
		self._query = """
        SELECT date_time, price
        FROM fx_prices
        WHERE symbol = $1
        ORDER BY date_time
        """
		self._parameters = (fx_code,)
		self._output_type = InstrumentCurrency

	@property
	def parameters(self) -> tuple:
		return self._parameters
