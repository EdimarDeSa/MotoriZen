import calendar
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Any, Sequence

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Label, Null, RowMapping, null
from sqlalchemy.orm import Session, scoped_session

from DB.Models.range_model import RangeModel
from DB.Querys import RegisterQueryManager
from DB.Querys.user_query_manager import UserQueryManager
from Enums.reports_daily_enum import ReportsDailyEnum
from Enums.reports_mean_enum import ReportsMeanEnum
from Enums.reports_monthly_enum import ReportsMonthlyEnum
from Enums.reports_total_enum import ReportsTotalEnum
from Enums.reports_weekly_enum import ReportsWeeklyEnum
from Enums.reports_yearly_enum import ReportsYearlyEnum
from Utils.constants import *
from Utils.custom_primitive_types import DataFrameType, Periodes

from .base_repository import BaseRepository


class ReportsRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._register_querys = RegisterQueryManager()
        self._user_querys = UserQueryManager()

    def select_report_query(self, report: StrEnum) -> Label[Any]:
        self.logger.debug("Starting select_report_query")

        self.logger.debug(f"Matching report: {report}")
        _query: Label[Any] | Null = null()

        match report:
            case ReportsMeanEnum.MEAN_CONSUMPTION_PER_DISTANCE:
                _query = self._register_querys.mean_consumption_per_distance()

            case ReportsMeanEnum.MEAN_CONSUMPTION_PER_TRIP:
                _query = self._register_querys.mean_consumption_per_trip()

            case ReportsMeanEnum.MEAN_CONSUMPTION_PER_WORKING_HOUR:
                _query = self._register_querys.mean_consumption_per_working_hour()

            case ReportsMeanEnum.MEAN_CONSUMPTION_PER_WORKING_MINUTE:
                _query = self._register_querys.mean_consumption_per_working_minute()

            case ReportsMeanEnum.MEAN_DISTANCE:
                _query = self._register_querys.mean_distance()

            case ReportsMeanEnum.MEAN_NUMBER_OF_TRIPS:
                _query = self._register_querys.mean_number_of_trips()

            case ReportsMeanEnum.MEAN_WORKING_TIME:
                _query = self._register_querys.mean_working_time()

            case ReportsMeanEnum.MEAN_WORKING_TIME_PER_TRIP:
                _query = self._register_querys.mean_working_time_per_trip()

            case ReportsMeanEnum.MEAN_VALUE_RECEIVED:
                _query = self._register_querys.mean_value_received()

            case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_CONSUMPTION:
                _query = self._register_querys.mean_value_received_per_consumption()

            case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_DISTANCE:
                _query = self._register_querys.mean_value_received_per_distance()

            case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_TRIP:
                _query = self._register_querys.mean_value_received_per_trip()

            case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_WORKING_HOUR:
                _query = self._register_querys.mean_value_received_per_working_hour()

            case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_WORKING_MINUTE:
                _query = self._register_querys.mean_value_received_per_working_minute()

            case (
                ReportsTotalEnum.TOTAL_CONSUMPTION
                | ReportsDailyEnum.DAILY_CONSUMPTION
                | ReportsWeeklyEnum.WEEKLY_CONSUMPTION
                | ReportsMonthlyEnum.MONTHLY_CONSUMPTION
                | ReportsYearlyEnum.YEARLY_CONSUMPTION
            ):
                _query = self._register_querys.total_consumption()

            case (
                ReportsTotalEnum.TOTAL_DISTANCE
                | ReportsDailyEnum.DAILY_DISTANCE
                | ReportsWeeklyEnum.WEEKLY_DISTANCE
                | ReportsMonthlyEnum.MONTHLY_DISTANCE
                | ReportsYearlyEnum.YEARLY_DISTANCE
            ):
                _query = self._register_querys.total_distance()

            case (
                ReportsTotalEnum.TOTAL_WORKING_TIME
                | ReportsDailyEnum.DAILY_WORKING_TIME
                | ReportsWeeklyEnum.WEEKLY_WORKING_TIME
                | ReportsMonthlyEnum.MONTHLY_WORKING_TIME
                | ReportsYearlyEnum.YEARLY_WORKING_TIME
            ):
                _query = self._register_querys.total_working_time()

            case (
                ReportsTotalEnum.TOTAL_NUMBER_OF_TRIPS
                | ReportsDailyEnum.DAILY_NUMBER_OF_TRIPS
                | ReportsWeeklyEnum.WEEKLY_NUMBER_OF_TRIPS
                | ReportsMonthlyEnum.MONTHLY_NUMBER_OF_TRIPS
                | ReportsYearlyEnum.YEARLY_NUMBER_OF_TRIPS
            ):
                _query = self._register_querys.total_number_of_trips()

            case (
                ReportsTotalEnum.TOTAL_VALUE_RECEIVED
                | ReportsDailyEnum.DAILY_VALUE_RECEIVED
                | ReportsWeeklyEnum.WEEKLY_VALUE_RECEIVED
                | ReportsMonthlyEnum.MONTHLY_VALUE_RECEIVED
                | ReportsYearlyEnum.YEARLY_VALUE_RECEIVED
            ):
                _query = self._register_querys.total_value_received()

        return _query.label(report)

    def select_reports(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        date_: RangeModel[date],
        car_ids: Sequence[uuid.UUID],
        report_list: list[Label[Any]],
    ) -> DataFrameType:
        self.logger.debug("Starting select_reports")

        try:
            query = self._user_querys.select_reports(id_user, car_ids, date_, report_list)

            self.logger.debug(f"Query: {query}")

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            return {
                result[ID_CAR]: {
                    report: self.__format_value(result[report]) for report in result.keys() if report != ID_CAR
                }
                for result in results
            }

        except Exception as e:
            raise e

    def select_periodicaly_reports(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        date_: RangeModel[date],
        car_ids: Sequence[uuid.UUID],
        periode: Periodes,
        report_list: list[Label[Any]],
    ) -> DataFrameType:
        self.logger.debug("Starting select_periodicaly_reports")

        try:
            query = self._user_querys.select_periodicaly_report(id_user, car_ids, date_, periode, report_list)

            self.logger.debug(f"Query: {query}")

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()
            import json

            self.logger.debug(f"Results: {json.dumps(jsonable_encoder(results))}")

            return self.__format_data_frame(results, periode)

        except Exception as e:
            raise e

    def __format_data_frame(self, results: Sequence[RowMapping], periode: Periodes) -> DataFrameType:
        data_frame: DataFrameType = {}
        for result in results:
            if result[ID_CAR] not in data_frame.keys():
                data_frame[result[ID_CAR]] = {}

            for report in result.keys():
                if report in [ID_CAR, PERIODE_START_DATE]:
                    continue

                if report not in data_frame[result[ID_CAR]].keys():
                    data_frame[result[ID_CAR]][report] = {}

                _key = self.__create_periode_key(result[PERIODE_START_DATE], periode)
                data_frame[result[ID_CAR]][report][_key] = self.__format_value(result[report])
        return data_frame

    def __create_periode_key(self, date_: date, periode: Periodes) -> str:
        initial_date = self.__strfdate(date_)
        final_date = self.__calculate_final_date(date_, periode)
        return f"{initial_date} ~ {final_date}"

    def __format_value(self, value: Any) -> int | float | str:
        if value is None:
            return "Not implemented yet."

        if isinstance(value, timedelta):
            time_ = datetime.min + value
            return self.__strftime(time_)

        if isinstance(value, float | Decimal):
            return round(float(value), 2)

        if isinstance(value, int):
            return value

        return str(value)

    def __calculate_final_date(self, initial_date: date, periode: Periodes) -> str:
        date_ = initial_date

        if periode == WEEKLY:
            date_ = initial_date + timedelta(days=6)

        if periode == MONTHLY:
            last_day = calendar.monthrange(initial_date.year, initial_date.month)[1]
            date_ = date(initial_date.year, initial_date.month, last_day)

        if periode == YEARLY:
            last_day = calendar.monthrange(initial_date.year, 12)[1]
            date_ = date(initial_date.year, 12, last_day)

        return self.__strfdate(date_)

    def __strfdate(self, date_: date) -> str:
        return date_.strftime(r"%d-%m-%Y")

    def __strftime(self, time_: datetime) -> str:
        return time_.strftime(r"%H:%M:%S")
