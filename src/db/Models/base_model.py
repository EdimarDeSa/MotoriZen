from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class NewBaseModelDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseModelDb(NewBaseModelDb):
    updated_at: datetime = Field(description=ModelsDescriptionTexts.updated_at)
    created_at: datetime = Field(description=ModelsDescriptionTexts.created_at)
    deleted_at: datetime = Field(description=ModelsDescriptionTexts.deleted_at)
