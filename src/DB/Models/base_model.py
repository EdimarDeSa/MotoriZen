from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NewBaseModelDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseModelDb(NewBaseModelDb):
    last_update: datetime = Field(description="Last update of the user")
    creation: datetime = Field(description="Creation of the user")
