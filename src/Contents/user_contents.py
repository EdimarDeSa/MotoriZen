from db.Models import UserModel, UserNewModel
from Responses.base_response import BaseContent


class UserMeContent(BaseContent):
    data: UserModel


class UserNewContent(BaseContent):
    data: UserNewModel


class UserUpdatedContent(BaseContent):
    data: UserModel
