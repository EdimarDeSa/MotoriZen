from db.Models import UserModel
from db.Models.user_model import NewUserModel
from Responses.base_response import BaseContent


class UserMeContent(BaseContent):
    data: UserModel


class UserNewContent(BaseContent):
    data: NewUserModel


class UserUpdatedContent(BaseContent):
    data: UserModel
