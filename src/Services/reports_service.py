from datetime import date, time, timedelta
from typing import Any, Mapping, Sequence, cast

from sqlalchemy import Label

from DB.Models.range_model import RangeModel
from DB.Models.reports_query_model import ReportsQueryModel, ReportsType
from Enums import (
    ReportsDailyEnum,
    ReportsMeanEnum,
    ReportsMonthlyEnum,
    ReportsTotalEnum,
    ReportsWeeklyEnum,
    ReportsYearlyEnum,
)
from Repositories.reports_repository import ReportsRepository
from Utils.constants import DAILY, MONTHLY, WEEKLY, YEARLY
from Utils.custom_primitive_types import DataFrameType, Periodes
from Utils.data_frame import DataFrame
from Utils.redis_handler import RedisHandler

from .base_service import BaseService


class ReportsService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self._reports_reporitosy = ReportsRepository()
        self._cache_handler = RedisHandler()
        self.create_logger(__name__)

    def get_reports(self, id_user: str, reports_query: ReportsQueryModel) -> DataFrame:
        self.logger.debug("Starting get_reports")

        try:
            self.logger.debug("Creating defaults")
            db_session = self.create_session(write=False)

            data_frame = DataFrame()
            reports = reports_query.reports or self.__list_all_reports()
            date_ = reports_query.date_ or self.__default_range_date()
            car_ids = reports_query.car_ids or []
            report_querys: list[Label[Any]] = []
            periodicaly_querys: dict[Periodes, list[Label[Any]]] = {
                DAILY: [],
                WEEKLY: [],
                MONTHLY: [],
                YEARLY: [],
            }

            self.logger.debug("Filtering and mounting reports")
            for report in reports:
                _query = self._reports_reporitosy.select_report_query(report)
                if isinstance(report, ReportsDailyEnum):
                    periodicaly_querys[DAILY].append(_query)

                elif isinstance(report, ReportsWeeklyEnum):
                    periodicaly_querys[WEEKLY].append(_query)

                elif isinstance(report, ReportsMonthlyEnum):
                    periodicaly_querys[MONTHLY].append(_query)

                elif isinstance(report, ReportsYearlyEnum):
                    periodicaly_querys[YEARLY].append(_query)

                else:
                    report_querys.append(_query)

            if report_querys:
                report_data = self._reports_reporitosy.select_reports(
                    db_session, id_user, date_, car_ids, report_querys
                )
                data_frame.insert_reports(report_data)

            for key, report_list in periodicaly_querys.items():
                if report_list:
                    report_data = self._reports_reporitosy.select_periodicaly_reports(
                        db_session, id_user, date_, car_ids, key, report_list
                    )
                    data_frame.insert_reports(report_data)

            return data_frame

        except Exception as e:
            raise e

    def __default_range_date(self) -> RangeModel[date]:
        return RangeModel[date](start=(date.today() - timedelta(days=date.today().weekday())), end=date.today())

    def __list_all_reports(self) -> ReportsType:
        reports = [
            report
            for enum in [
                ReportsTotalEnum,
                ReportsMeanEnum,
                ReportsDailyEnum,
                ReportsWeeklyEnum,
                ReportsMonthlyEnum,
                ReportsYearlyEnum,
            ]
            for report in enum
        ]
        return cast(ReportsType, reports)
