from Contents.base_content import BaseContent
from db.Models import RegisterModel, RegisterQueryResponseModel


class RegisterContent(BaseContent):
    data: RegisterModel


class RegistersContent(BaseContent):
    data: RegisterQueryResponseModel
