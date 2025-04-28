from pydantic import BaseModel, Field

from db.Models.vehicle_models.vehicle_query_filters_model import VehicleQueryFiltersModel
from db.Models.vehicle_models.vehicle_query_options import VehicleQueryOptionsModel
from Utils.Internacionalization import ModelsDescriptionTexts


class VehicleQueryModel(BaseModel):
    query_filters: VehicleQueryFiltersModel = Field(
        default_factory=VehicleQueryFiltersModel, description=ModelsDescriptionTexts.QUERY_FILTERS
    )
    query_options: VehicleQueryOptionsModel = Field(
        default_factory=VehicleQueryOptionsModel, description=ModelsDescriptionTexts.QUERY_OPTIONS
    )
