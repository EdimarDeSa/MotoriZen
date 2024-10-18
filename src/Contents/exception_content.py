from pydantic import Field

from Contents.base_content import BaseContent
from Enums import MotorizenErrorEnum
from ErrorHandler import ErrorModel


class ExceptionContent(BaseContent):
    rc: MotorizenErrorEnum = Field(description="Error mapped from MotorizenErrorEnum")
    data: ErrorModel = Field(description="Model with error details")
