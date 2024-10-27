from pydantic import BaseModel, Field

from db.Models.car_query_filters_model import CarQueryFiltersModel
from db.Models.car_query_options import CarQueryOptionsModel


class CarQueryModel(BaseModel):
    query_filters: CarQueryFiltersModel = Field(default_factory=CarQueryFiltersModel)
    query_options: CarQueryOptionsModel = Field(default_factory=CarQueryOptionsModel)
