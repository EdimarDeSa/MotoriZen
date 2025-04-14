from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class NewBaseModelDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseModelDb(NewBaseModelDb):
    updated_at: datetime = Field(description=ModelsDescriptionTexts.UPDATED_AT)
    created_at: datetime = Field(description=ModelsDescriptionTexts.CREATED_AT)
    deleted_at: datetime | None = Field(description=ModelsDescriptionTexts.DELETED_AT)
