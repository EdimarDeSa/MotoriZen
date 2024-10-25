from db.Models import NewUserModel, UserModel
from Responses.base_response import BaseContent


class UserMeContent(BaseContent):
    data: UserModel


class UserNewContent(BaseContent):
    data: NewUserModel


class UserUpdatedContent(BaseContent):
    data: UserModel
