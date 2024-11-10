import uuid
from typing import Any, Literal

from pydantic import Field

from Contents.base_content import BaseContent
from DB.Models.report_response_model import ReportResponseModel


class ReportsContent(BaseContent):
    data: ReportResponseModel = Field(default_factory=dict, description="Return data, if any.")
