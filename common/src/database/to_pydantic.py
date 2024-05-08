from typing import Any, Optional, Type

from pydantic import BaseModel, ValidationError


def convert_to_pydantic(data: Optional[Any], model: Type[BaseModel]):
	if isinstance(data, dict):
		return model(**data)
	else:
		raise ValidationError('Input data is not a dictionary')
