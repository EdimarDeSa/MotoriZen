import uuid
from datetime import date, timedelta
from typing import Any, Mapping, Sequence

from sqlalchemy import RowMapping
from sqlalchemy.orm import Session, scoped_session

from DB.Models.range_model import RangeModel
from Enums import ReportsDailyEnum
from Repositories.base_report_repository import BaseReportRepository
from Repositories.base_repository import BaseRepository


class ReportsDailyRepository(BaseRepository, BaseReportRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)

    def get_daily_report(
        self,
        report: ReportsDailyEnum,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
    ) -> Sequence[Mapping[str, Any]]:
        self.logger.debug("Starting get_mean_report")

        try:
            self.logger.debug(f"Matching report: {report}")
            match report:
                case ReportsDailyEnum.DAILY_COMSUPTION:
                    return self.__select_daily_comsuption(db_session, id_user, car_ids, date_, report.value)

                case ReportsDailyEnum.DAILY_DISTANCE:
                    return self.__select_daily_distance(db_session, id_user, car_ids, date_, report.value)

                case ReportsDailyEnum.DAILY_WORKING_TIME:
                    return self.__select_daily_working_time(db_session, id_user, car_ids, date_, report.value)

                case ReportsDailyEnum.DAILY_NUMBER_OF_TRIPS:
                    return self.__select_daily_number_of_trips(db_session, id_user, car_ids, date_, report.value)

                case ReportsDailyEnum.DAILY_VALUE_RECEIVED:
                    return self.__select_daily_value_received(db_session, id_user, car_ids, date_, report.value)

                case _:
                    return self.return_not_implemented(report)

        except Exception as e:
            raise e

    def __select_daily_comsuption(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float | int | str]]]:

        self.logger.debug("Starting __select_daily_comsuption")
        try:
            query = self.querys.select_comsuption_per_day(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Daily consumption: {results}")

            if results is None:
                results = self.default_date(report, car_ids)

            return self.return_periodic(results, report, timedelta(days=0))

        except Exception as e:
            raise e

    def __select_daily_distance(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float | int | str]]]:

        self.logger.debug("Starting __select_daily_distance")
        try:
            query = self.querys.select_daily_distance(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Daily distance travelled: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_periodic(results, report, timedelta(days=0))

        except Exception as e:
            raise e

    def __select_daily_working_time(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float | int | str]]]:

        self.logger.debug("Starting __select_daily_working_time")
        try:
            query = self.querys.select_daily_working_time(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Daily working time: {results}")

            if results is None:
                results = self.default_time(report, car_ids)

            return self.return_periodic(results, report, timedelta(days=0))

        except Exception as e:
            raise e

    def __select_daily_number_of_trips(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float | int | str]]]:

        self.logger.debug("Starting __select_daily_number_of_trips")
        try:
            query = self.querys.select_daily_number_of_trips(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Daily number of trips: {results}")

            if results is None:
                results = self.default_time(report, car_ids)

            return self.return_periodic(results, report, timedelta(days=0))

        except Exception as e:
            raise e

    def __select_daily_value_received(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | dict[str, float | int | str]]]:

        self.logger.debug("Starting __select_daily_value_received")
        try:
            query = self.querys.select_daily_value_received(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Daily value received: {results}")

            if results is None:
                results = self.default_time(report, car_ids)

            return self.return_periodic(results, report, timedelta(days=0))

        except Exception as e:
            raise e
