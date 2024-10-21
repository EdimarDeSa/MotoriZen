from pydantic import Field

from Contents.base_content import BaseContent
from Enums import MotoriZenErrorEnum
from ErrorHandler import ErrorModel


class ExceptionContent(BaseContent):
    rc: MotoriZenErrorEnum = Field(description="Error mapped from MotorizenErrorEnum")
    data: ErrorModel = Field(description="Model with error details")
