from typing import TypeVar

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_pydantic(item: dict | None, model: type[T]) -> T | None:
    if item is None:
        return None
    return model(**item)


def convert_dataframe_to_series(data_frame: pd.DataFrame, index: str, values: str) -> pd.Series:
    sorted_data_frame = data_frame.sort_values(by=index)
    return pd.Series(sorted_data_frame[values].values, index=sorted_data_frame[index])


def convert_pandas_to_bytes(df: pd.DataFrame | pd.Series) -> bytes:
    table = pa.Table.from_pandas(df)
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_file(sink, table.schema)
    writer.write_table(table)
    writer.close()
    return sink.getvalue().to_pybytes()
