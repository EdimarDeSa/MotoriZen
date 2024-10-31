import uuid
from datetime import date, time, timedelta
from enum import StrEnum
from typing import Any, Literal, Mapping, Sequence, cast

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
from Repositories.reports_daily_repository import ReportsDailyRepository
from Repositories.reports_mean_repository import ReportsMeanRepository
from Repositories.reports_total_repository import ReportsTotalRepository
from Services.base_service import BaseService
from Utils.redis_handler import RedisHandler


class ReportsService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self._reports_total_repository = ReportsTotalRepository()
        self._reports_mean_repository = ReportsMeanRepository()
        self._reports_daily_repository = ReportsDailyRepository()
        self._cache_handler = RedisHandler()
        self.create_logger(__name__)

    def get_reports(
        self, id_user: str, reports_query: ReportsQueryModel
    ) -> dict[uuid.UUID | Literal["-1"], dict[str, Any]]:
        self.logger.debug("Starting get_reports")
        db_session = self.create_session(write=False)
        data_set: dict[uuid.UUID | Literal["-1"], dict[str, Any]] = {}

        try:
            reports = reports_query.reports or self.__list_all_reports()
            date_ = reports_query.date_ or self.__default_range_date()
            car_ids = reports_query.car_ids or []

            for report in reports:
                hash_data = {
                    "report": report,
                    "car_ids": car_ids,
                    "date": date_.model_dump(mode="json"),
                }

                hash_key = self.create_hash_key(hash_data)
                reports_data: Sequence[Mapping[str, Any]] | None = None

                # reports_data: Sequence[Mapping[str, Any]] | None = self.get_user_cached_data(RedisDbsEnum.REPORTS, id_user, hash_key)

                if reports_data is None:
                    reports_data = []

                    if isinstance(report, ReportsTotalEnum):
                        reports_data = self._reports_total_repository.get_total_report(
                            report, db_session, id_user, car_ids, date_
                        )

                    if isinstance(report, ReportsMeanEnum):
                        reports_data = self._reports_mean_repository.get_mean_report(
                            report, db_session, id_user, car_ids, date_
                        )

                    if isinstance(report, ReportsDailyEnum):
                        reports_data = self._reports_daily_repository.get_daily_report(
                            report, db_session, id_user, car_ids, date_
                        )

                    # self.insert_user_cache_data(RedisDbsEnum.REPORTS, id_user, hash_key, reports_data)
                    for report_data in reports_data:
                        if not isinstance(report_data, dict):
                            continue

                        car = report_data.pop("id_car")

                        if car in data_set.keys():
                            data_set[car].update(report_data)
                        else:
                            data_set[car] = report_data

            return data_set

        except Exception as e:
            raise e

    def __default_range_date(self) -> RangeModel[date]:
        return RangeModel[date](start=(date.today() - timedelta(days=date.today().weekday())), end=date.today())

    def __default_range_time(self) -> RangeModel[time]:
        return RangeModel[time](start=time(0, 0), end=time(23, 59))

    def __list_all_reports(self) -> ReportsType:
        reports = [
            report
            for enum in [
                # ReportsTotalEnum,
                # ReportsMeanEnum,
                ReportsDailyEnum,
                # ReportsWeeklyEnum,
                # ReportsMonthlyEnum,
                # ReportsYearlyEnum,
            ]
            for report in enum
        ]
        return cast(ReportsType, reports)
