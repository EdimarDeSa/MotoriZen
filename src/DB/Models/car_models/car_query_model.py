from pydantic import BaseModel, Field

from DB.Models.car_models.car_query_filters_model import CarQueryFiltersModel
from DB.Models.car_models.car_query_options import CarQueryOptionsModel
from Utils.Internacionalization import ModelsDescriptionTexts


class CarQueryModel(BaseModel):
    query_filters: CarQueryFiltersModel = Field(
        default_factory=CarQueryFiltersModel, description=ModelsDescriptionTexts.QUERY_FILTERS
    )
    query_options: CarQueryOptionsModel = Field(
        default_factory=CarQueryOptionsModel, description=ModelsDescriptionTexts.QUERY_OPTIONS
    )
