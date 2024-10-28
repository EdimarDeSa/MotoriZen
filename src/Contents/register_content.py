from Contents.base_content import BaseContent
from DB.Models import RegisterModel, RegisterQueryResponseModel


class RegisterContent(BaseContent):
    data: RegisterModel | list[RegisterModel]


class RegistersContent(BaseContent):
    data: RegisterQueryResponseModel
