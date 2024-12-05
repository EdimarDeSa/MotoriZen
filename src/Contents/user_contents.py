from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models import UserModel, UserNewModel
from Utils.Internacionalization import ModelsDescriptionTexts


class UserMeContent(BaseContent):
    data: UserModel = Field(description=ModelsDescriptionTexts.BASE_DATA)


class UserNewContent(BaseContent):
    data: UserNewModel = Field(description=ModelsDescriptionTexts.BASE_DATA)


class UserUpdatedContent(BaseContent):
    data: UserModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
