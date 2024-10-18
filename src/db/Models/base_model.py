from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseModelDb(BaseModel):
    model_config = ConfigDict(str_to_lower=True, from_attributes=True)

    last_update: datetime = Field(serialization_alias="lastUpdate", description="Last update of the user")
    creation: datetime = Field(description="Creation of the user")


class NewBaseModelDb(BaseModel):
    model_config = ConfigDict(str_to_lower=True, from_attributes=True)
