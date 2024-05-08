from typing import Any

import pandas as pd


def to_pydantic(item: Any | None, model: Any) -> Any:
	if item is None:
		return None
	else:
		return model(**item)


def to_series(items: list, model: Any) -> pd.Series:
	return pd.Series([model(**item) for item in items])
