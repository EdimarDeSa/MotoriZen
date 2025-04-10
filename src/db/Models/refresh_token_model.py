from pydantic import BaseModel, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class RefreshTokenModel(BaseModel):
    refresh_token: str = Field(description=ModelsDescriptionTexts.REFRESH_TOKEN)
