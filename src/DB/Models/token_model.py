from pydantic import BaseModel, Field

from Utils.Internacionalization import ModelsDescriptionTexts


class TokenModel(BaseModel):
    access_token: str = Field(description=ModelsDescriptionTexts.ACCESS_TOKEN)
    token_type: str = Field(description=ModelsDescriptionTexts.TOKEN_TYPE)
    expires_in: int = Field(description=ModelsDescriptionTexts.EXPIRES_IN)
    refresh_expires_in: int = Field(description=ModelsDescriptionTexts.REFRESH_EXPIRES_IN)
    refresh_token: str = Field(description=ModelsDescriptionTexts.REFRESH_TOKEN)
    scope: str = Field(description=ModelsDescriptionTexts.SCOPE)
    session_state: str = Field(description=ModelsDescriptionTexts.SESSION_STATE)
    not_before_policy: int | None = Field(
        default=None, validation_alias="not-before-policy", description=ModelsDescriptionTexts.NOT_BEFORE_POLICY
    )
