from typing import List, Type

from pandera import DataFrameModel
from pydantic import BaseModel


def validate_data_with_pandera(dataframe, schema: Type[DataFrameModel]):
    return schema.validate(dataframe)


def convert_to_pydantic(data: dict, model: Type[BaseModel]):
    return model(**data)


def convert_list_to_pydantic(data: List[dict], model: Type[BaseModel]) -> List[BaseModel]:
    return [model(**item) for item in data]
