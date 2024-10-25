from pydantic import BaseModel, Field

from db.Models.car_query_options import CarQueryOptionsModel
from db.Models.car_query_params_model import CarQueryParamsModel


class CarQueryModel(BaseModel):
    query_params: CarQueryParamsModel = Field(default_factory=CarQueryParamsModel)
    query_options: CarQueryOptionsModel = Field(default_factory=CarQueryOptionsModel)
