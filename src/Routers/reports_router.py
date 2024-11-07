from fastapi import APIRouter, Request

from Contents.reports_content import ReportsContent
from DB.Models import ReportsQueryModel
from DB.Models.report_reponse_metadata_model import ReportResponseMetadataModel
from DB.Models.report_response_model import ReportResponseModel
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Responses import Ok
from Routers.base_router import BaseRouter
from Services.reports_service import ReportsService
from Utils.custom_types import CurrentActiveUser
from Utils.data_frame import DataFrame


class ReportsRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.reports_service = ReportsService()
        self.router = APIRouter(prefix="/reports", tags=["Reports"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/get-reports", self.get_reports, response_model=ReportsContent, methods=["POST"])

    def get_reports(self, request: Request, user_data: CurrentActiveUser, reports_query: ReportsQueryModel) -> Ok:
        self.logger.debug("Starting get_reports")

        try:
            response: DataFrame = self.reports_service.get_reports(str(user_data.id_user), reports_query)
            keys_ = list(response.keys())
            total_cars = len(keys_)
            total_results = 0
            for key in keys_:
                total_results += len(response[key])

            report_response = ReportResponseModel(
                results=response,
                metadata=ReportResponseMetadataModel(
                    total_cars=total_cars,
                    total_results=total_results,
                    total_reports_selected=reports_query.reports.__len__() if reports_query.reports else 0,
                    total_bites=response.nbytes,
                ),
            )

            content = ReportsContent(data=report_response)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()
