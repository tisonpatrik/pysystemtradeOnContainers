from pydantic import BaseModel


class ForecastRequest(BaseModel):
	rule: str
	speed: int
	symbol: str
