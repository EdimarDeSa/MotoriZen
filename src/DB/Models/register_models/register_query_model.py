from pydantic import BaseModel, Field

from DB.Models.register_models.register_query_filters_model import RegisterQueryFiltersModel
from DB.Models.register_models.register_query_options import RegisterQueryOptionsModel
from Utils.Internacionalization import ModelsDescriptionTexts


class RegistersQueryModel(BaseModel):
    query_filters: RegisterQueryFiltersModel = Field(
        default_factory=RegisterQueryFiltersModel, description=ModelsDescriptionTexts.QUERY_FILTERS
    )
    query_options: RegisterQueryOptionsModel = Field(
        default_factory=RegisterQueryOptionsModel, description=ModelsDescriptionTexts.QUERY_OPTIONS
    )
