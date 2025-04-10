from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class NewBaseModelDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseModelDb(NewBaseModelDb):
    last_update: datetime = Field(description=ModelsDescriptionTexts.LAST_UPDATE)
    creation: datetime = Field(description=ModelsDescriptionTexts.CREATION)
