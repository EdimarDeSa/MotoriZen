from pydantic import BaseModel, Field

from db.Models import RegisterQueryFiltersModel, RegisterQueryOptionsModel


class RegistersQueryModel(BaseModel):
    query_filters: RegisterQueryFiltersModel = Field(default_factory=RegisterQueryFiltersModel)
    query_options: RegisterQueryOptionsModel = Field(default_factory=RegisterQueryOptionsModel)
