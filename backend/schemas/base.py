from typing import Any

import humps
import ujson
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


# * Pure pydantic model without any alias generator
class PureBaseModel(BaseModel):
    def jsonable_encoder(self, **kwargs: Any) -> Any:
        return jsonable_encoder(self, **kwargs)

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        use_enum_values = True
        json_loads = ujson.loads
        json_dumps = ujson.dumps


# * Camel alias generator model
class CamelizedBaseModel(PureBaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        use_enum_values = True
        json_loads = ujson.loads
        json_dumps = ujson.dumps
        alias_generator = humps.camelize
