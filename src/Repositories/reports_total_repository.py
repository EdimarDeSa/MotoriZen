import uuid
from datetime import date, time
from typing import Any, Mapping, Sequence

from sqlalchemy import RowMapping
from sqlalchemy.orm import Session, scoped_session

from DB.Models.range_model import RangeModel
from Enums import ReportsTotalEnum
from Repositories.base_report_repository import BaseReportRepository
from Repositories.base_repository import BaseRepository


class ReportsTotalRepository(BaseRepository, BaseReportRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)

    def get_total_report(
        self,
        report: ReportsTotalEnum,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
    ) -> Sequence[Mapping[str, Any]]:
        self.logger.debug("Starting get_total_report")

        try:
            self.logger.debug(f"Matching report: {report}")
            match report:
                case ReportsTotalEnum.TOTAL_COMSUPTION:
                    return self.__select_total_consumption(db_session, id_user, car_ids, date_, report.value)

                case ReportsTotalEnum.TOTAL_DISTANCE:
                    return self.__select_total_distance(db_session, id_user, car_ids, date_, report.value)

                case ReportsTotalEnum.TOTAL_WORKING_TIME:
                    return self.__select_total_working_time(db_session, id_user, car_ids, date_, report.value)

                case ReportsTotalEnum.TOTAL_NUMBER_OF_TRIPS:
                    return self.__select_total_number_of_trips(db_session, id_user, car_ids, date_, report.value)

                case ReportsTotalEnum.TOTAL_VALUE_RECEIVED:
                    return self.__select_total_value_received(db_session, id_user, car_ids, date_, report.value)

                case _:
                    return self.return_not_implemented(report)

        except Exception as e:
            raise e

    def __select_total_consumption(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __get_total_consumption")
        try:
            query = self.querys.select_total_consumption(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Total consumption: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_total_distance(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __get_total_distance")
        try:
            query = self.querys.select_total_distance(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Total distance: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_total_working_time(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | str]]:
        self.logger.debug("Starting __get_total_working_time")
        try:
            query = self.querys.select_total_working_time(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Total working time: {results}")

            if results is None:
                results = self.default_time(report, car_ids)

            return self.return_time(results)

        except Exception as e:
            raise e

    def __select_total_number_of_trips(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | int]]:
        self.logger.debug("Starting __get_total_number_of_trips")
        try:
            query = self.querys.select_total_number_of_trips(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Total number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_total_value_received(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_total_value_received")
        try:
            query = self.querys.select_total_value_received(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Total value recived: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e
