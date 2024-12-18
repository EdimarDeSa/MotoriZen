import calendar
import json
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
from Enums import AggregationIntervalEnum
from Enums.report_enum import ReportsEnum
from Utils.constants import *
from Utils.custom_primitive_types import DataFrameType

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
            ### Distance reports ###
            case ReportsEnum.MEAN_DISTANCE:
                _query = self._register_querys.mean_distance()

            case ReportsEnum.MEAN_DISTANCE_PER_TRIP:
                _query = self._register_querys.mean_distance_per_trip()

            case ReportsEnum.MEAN_DISTANCE_PER_WORKING_HOUR:
                _query = self._register_querys.mean_distance_per_working_hour()

            case ReportsEnum.MEAN_DISTANCE_PER_WORKING_MINUTE:
                _query = self._register_querys.mean_distance_per_working_minute()

            case ReportsEnum.TOTAL_DISTANCE:
                _query = self._register_querys.total_distance()

            ### Working time reports ###
            case ReportsEnum.MEAN_WORKING_TIME:
                _query = self._register_querys.mean_working_time()

            case ReportsEnum.MEAN_WORKING_TIME_PER_TRIP:
                _query = self._register_querys.mean_working_time_per_trip()

            case ReportsEnum.MEAN_WORKING_TIME_PER_DISTANCE:
                _query = self._register_querys.mean_working_time_per_distance()

            case ReportsEnum.TOTAL_WORKING_TIME:
                _query = self._register_querys.total_working_time()

            ### Consumption reports ###
            case ReportsEnum.MEAN_CONSUPTION_PER_DISTANCE:
                _query = self._register_querys.mean_consuption_per_distance()

            case ReportsEnum.MEAN_CONSUPTION_PER_TRIP:
                _query = self._register_querys.mean_consuption_per_trip()

            case ReportsEnum.MEAN_CONSUPTION_PER_WORKING_HOUR:
                _query = self._register_querys.mean_consuption_per_working_hour()

            case ReportsEnum.MEAN_CONSUPTION_PER_WORKING_MINUTE:
                _query = self._register_querys.mean_consuption_per_working_minute()

            case ReportsEnum.TOTAL_CONSUPTION:
                _query = self._register_querys.total_consumption()

            case ReportsEnum.TOTAL_CONSUMPTION_PER_TRIP:
                _query = self._register_querys.total_consumption_per_trip()

            ### Value reports ###
            case ReportsEnum.MEAN_VALUE_RECEIVED:
                _query = self._register_querys.mean_value_received()

            case ReportsEnum.MEAN_VALUE_RECEIVED_PER_CONSUMPTION:
                _query = self._register_querys.mean_value_received_per_consumption()

            case ReportsEnum.MEAN_VALUE_RECEIVED_PER_DISTANCE:
                _query = self._register_querys.mean_value_received_per_distance()

            case ReportsEnum.MEAN_VALUE_RECEIVED_PER_TRIP:
                _query = self._register_querys.mean_value_received_per_trip()

            case ReportsEnum.MEAN_VALUE_RECEIVED_PER_WORKING_HOUR:
                _query = self._register_querys.mean_value_received_per_working_hour()

            case ReportsEnum.MEAN_VALUE_RECEIVED_PER_WORKING_MINUTE:
                _query = self._register_querys.mean_value_received_per_working_minute()

            case ReportsEnum.TOTAL_VALUE_RECEIVED:
                _query = self._register_querys.total_value_received()

            ### Number of trips reports ###
            case ReportsEnum.MEAN_NUMBER_OF_TRIPS:
                _query = self._register_querys.mean_number_of_trips()

            case ReportsEnum.MEAN_NUMBER_OF_TRIPS_PER_WORKING_HOUR:
                _query = self._register_querys.mean_number_of_trips_per_working_hour()

            case ReportsEnum.MEAN_NUMBER_OF_TRIPS_PER_WORKING_MINUTE:
                _query = self._register_querys.mean_number_of_trips_per_working_minute()

            case ReportsEnum.MEAN_NUMBER_OF_TRIPS_PER_10_KM:
                _query = self._register_querys.mean_number_of_trips_per_10_km()

            case ReportsEnum.TOTAL_NUMBER_OF_TRIPS:
                _query = self._register_querys.total_number_of_trips()

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

            self.logger.debug(f"Results: {json.dumps(jsonable_encoder(results))}")

            return {
                result[ID_CAR]: {
                    report: self.__format_value(result[report]) for report in result.keys() if report != ID_CAR
                }
                for result in results
            }

        except Exception as e:
            raise e

    def select_aggregated_reports(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        date_: RangeModel[date],
        car_ids: Sequence[uuid.UUID],
        aggregation_interval: AggregationIntervalEnum,
        report_list: list[Label[Any]],
    ) -> DataFrameType:
        self.logger.debug("Starting select_periodicaly_reports")

        try:
            query = self._user_querys.select_periodicaly_report(
                id_user, car_ids, date_, aggregation_interval, report_list
            )

            self.logger.debug(f"Query: {query}")

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Results: {json.dumps(jsonable_encoder(results))}")

            return self.__format_data_frame(results, aggregation_interval)

        except Exception as e:
            raise e

    def __format_data_frame(
        self, results: Sequence[RowMapping], aggregation_interval: AggregationIntervalEnum
    ) -> DataFrameType:
        data_frame: DataFrameType = {}
        for result in results:
            if result[ID_CAR] not in data_frame.keys():
                data_frame[result[ID_CAR]] = {}

            for report in result.keys():
                if report in [ID_CAR, PERIODE_START_DATE]:
                    continue

                if report not in data_frame[result[ID_CAR]].keys():
                    data_frame[result[ID_CAR]][report] = {}

                _key = self.__create_periode_key(result[PERIODE_START_DATE], aggregation_interval)
                data_frame[result[ID_CAR]][report][_key] = self.__format_value(result[report])
        return data_frame

    def __create_periode_key(self, date_: date, aggregation_interval: AggregationIntervalEnum) -> str:
        initial_date = self.__strfdate(date_)
        final_date = self.__calculate_final_date(date_, aggregation_interval)
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

    def __calculate_final_date(self, initial_date: date, aggregation_interval: AggregationIntervalEnum) -> str:
        date_ = initial_date

        match aggregation_interval:
            case AggregationIntervalEnum.WEEK:
                date_ = initial_date + timedelta(days=6)

            case AggregationIntervalEnum.MONTH:
                last_day = calendar.monthrange(initial_date.year, initial_date.month)[1]
                date_ = date(initial_date.year, initial_date.month, last_day)

            case AggregationIntervalEnum.YEAR:
                last_day = calendar.monthrange(initial_date.year, 12)[1]
                date_ = date(initial_date.year, 12, last_day)

        return self.__strfdate(date_)

    def __strfdate(self, date_: date) -> str:
        return date_.strftime(r"%d-%m-%Y")

    def __strftime(self, time_: datetime) -> str:
        return time_.strftime(r"%H:%M:%S")
