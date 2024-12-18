from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models.report_response_model import ReportResponseModel
from Utils.Internacionalization import ModelsDescriptionTexts


class ReportsContent(BaseContent):
    data: ReportResponseModel = Field(description=ModelsDescriptionTexts.BASE_DATA)
