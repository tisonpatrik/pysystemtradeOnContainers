from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True, order=True)
class InstrumentVolatilitySchema:
    index_column: str = field(default="unix_date_time")
    columns: Dict[str, str] = field(default_factory=lambda: {"price": "volatility"})
