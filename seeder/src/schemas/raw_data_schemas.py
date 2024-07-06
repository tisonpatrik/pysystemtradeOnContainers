import pandera as pa
from pandera.dtypes import Timestamp


class FxPricesSchema(pa.DataFrameModel):
	date_time: Timestamp
	symbol: str
	price: float = pa.Field(nullable=True)


class MultiplePricesSchema(pa.DataFrameModel):
	date_time: Timestamp
	symbol: str
	carry: float = pa.Field(nullable=True)
	carry_contract: int
	price: float = pa.Field(nullable=True)
	price_contract: int
	forward: float = pa.Field(nullable=True)
	forward_contract: int


class RollCalendarsSchema(pa.DataFrameModel):
	date_time: Timestamp
	symbol: str
	current_contract: int
	next_contract: int
	carry_contract: int


class AdjustedPricesSchema(pa.DataFrameModel):
	date_time: Timestamp
	symbol: str
	price: float = pa.Field(nullable=True)
