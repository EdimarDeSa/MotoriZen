from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    scope: str
    session_state: str
    not_before_policy: int = Field(validation_alias="not-before-policy")
