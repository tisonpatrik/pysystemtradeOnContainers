# base_model.py
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=False, validate_assignment=True)
