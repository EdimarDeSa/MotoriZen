import uuid
from datetime import date, timedelta
from typing import Any, Sequence

from sqlalchemy import Label

from DB.Models import ReportsQueryModel
from DB.Models.range_model import RangeModel
from DB.Models.report_reponse_metadata_model import ReportResponseMetadataModel
from DB.Models.report_response_model import ReportResponseModel
from Enums.report_enum import ReportsEnum
from Repositories.reports_repository import ReportsRepository
from Utils.custom_primitive_types import DataFrameType
from Utils.data_frame import DataFrame
from Utils.redis_handler import RedisHandler

from .base_service import BaseService


class ReportsService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self._reports_reporitosy = ReportsRepository()
        self._cache_handler = RedisHandler()
        self.create_logger(__name__)

    def get_reports(self, id_user: str, reports_query: ReportsQueryModel) -> ReportResponseModel:
        self.logger.debug("Starting get_reports")

        try:
            self.logger.debug("Creating defaults")
            db_session = self.create_session(write=False)

            self.logger.debug("Analyzing requested query")
            reports = reports_query.reports or self.__list_default_reports()
            time_frame = reports_query.time_frame or self.__default_time_frame()
            aggregation_interval = reports_query.aggregation_interval
            car_ids = reports_query.car_ids or self.__default_cars()
            data_frame = DataFrame()

            self.logger.debug("Filtering and mounting reports")

            report_querys: list[Label[Any]] = [
                self._reports_reporitosy.select_report_query(report) for report in reports
            ]

            report_data: DataFrameType | None = None

            if report_querys:
                report_data = (
                    self._reports_reporitosy.select_reports(db_session, id_user, time_frame, car_ids, report_querys)
                    if aggregation_interval is None
                    else self._reports_reporitosy.select_aggregated_reports(
                        db_session, id_user, time_frame, car_ids, aggregation_interval, report_querys
                    )
                )

            if report_data:
                data_frame.insert_reports(report_data)

            report_response = ReportResponseModel(
                results=data_frame,
                metadata=ReportResponseMetadataModel(
                    total_cars=data_frame.total_cars,
                    total_results=data_frame.total_results,
                    total_reports_selected=reports_query.reports.__len__() if reports_query.reports else 0,
                    total_bytes=data_frame.nbytes,
                ),
            )

            return report_response

        except Exception as e:
            raise e

    def _count_total_cars(self, data_frame: DataFrame) -> int:
        return len(data_frame.keys())

    def __default_time_frame(self) -> RangeModel[date]:
        return RangeModel[date](start=(date.today() - timedelta(days=date.today().weekday())), end=date.today())

    def __list_default_reports(self) -> Sequence[ReportsEnum]:
        return list(ReportsEnum)

    def __default_cars(self) -> Sequence[uuid.UUID]:
        return []
