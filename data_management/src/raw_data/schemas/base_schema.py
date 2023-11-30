from pydantic import BaseModel as PydanticBaseModel


class BaseSchema(PydanticBaseModel):
    file_name: str
    directory: str
