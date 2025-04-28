from pydantic import Field

from Contents.base_content import BaseContent
from Enums import MotoriZenErrorEnum
from ErrorHandler import ErrorModel
from Utils.Internacionalization import ModelsDescriptionTexts


class ExceptionContent(BaseContent):
    rc: int = Field(description=ModelsDescriptionTexts.EXCEPTIONS_RC)
    data: ErrorModel = Field(description=ModelsDescriptionTexts.EXCEPTIONS_DATA)
