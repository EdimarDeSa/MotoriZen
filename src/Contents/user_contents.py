from typing import Optional

from pydantic import Field

from db.Models import UserModel
from db.Models.user_model import NewUserModel
from Responses.base_response import BaseContent


class UserMeContent(BaseContent):
    data: UserModel


class UserNewContent(BaseContent):
    data: NewUserModel


class UserUpdatedContent(UserMeContent):
    data: UserModel


class UserDeleteContent(BaseContent):
    rc: Optional[int] = None
    data: None = None
    errors: None = None
