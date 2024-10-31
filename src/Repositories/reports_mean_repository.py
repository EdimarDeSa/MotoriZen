import uuid
from datetime import date
from typing import Any, Mapping, Sequence

from sqlalchemy import RowMapping
from sqlalchemy.orm import Session, scoped_session

from DB.Models.range_model import RangeModel
from Enums import ReportsMeanEnum
from Repositories.base_report_repository import BaseReportRepository
from Repositories.base_repository import BaseRepository


class ReportsMeanRepository(BaseRepository, BaseReportRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)

    def get_mean_report(
        self,
        report: ReportsMeanEnum,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
    ) -> Sequence[Mapping[str, Any]]:
        self.logger.debug("Starting get_mean_report")

        try:
            self.logger.debug(f"Matching report: {report}")
            match report:
                case ReportsMeanEnum.MEAN_COMSUPTION_PER_DISTANCE:
                    return self.__select_mean_comsuption_per_distance(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_COMSUPTION_PER_TRIP:
                    return self.__select_mean_comsuption_per_trip(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_COMSUPTION_PER_WORKING_HOUR:
                    return self.__select_mean_comsuption_per_working_hour(
                        db_session, id_user, car_ids, date_, report.value
                    )

                case ReportsMeanEnum.MEAN_COMSUPTION_PER_WORKING_MINUTE:
                    return self.__select_mean_comsuption_per_working_minute(
                        db_session, id_user, car_ids, date_, report.value
                    )

                case ReportsMeanEnum.MEAN_DISTANCE:
                    return self.__select_mean_distance(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_NUMBER_OF_TRIPS:
                    return self.__select_mean_number_of_trips(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_WORKING_TIME:
                    return self.__select_mean_working_time(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_WORKING_TIME_PER_TRIP:
                    return self.__select_mean_working_time_per_trip(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_VALUE_RECEIVED:
                    return self.__select_mean_value_received(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_COMSUPTION:
                    return self.__select_mean_value_received_per_comsuption(
                        db_session, id_user, car_ids, date_, report.value
                    )

                case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_DISTANCE:
                    return self.__select_mean_value_received_per_distance(
                        db_session, id_user, car_ids, date_, report.value
                    )

                case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_TRIP:
                    return self.__select_mean_value_received_per_trip(db_session, id_user, car_ids, date_, report.value)

                case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_WORKING_HOUR:
                    return self.__select_mean_value_received_per_working_hour(
                        db_session, id_user, car_ids, date_, report.value
                    )

                case ReportsMeanEnum.MEAN_VALUE_RECEIVED_PER_WORKING_MINUTE:
                    return self.__select_mean_value_received_per_working_minute(
                        db_session, id_user, car_ids, date_, report.value
                    )

                case _:
                    return self.return_not_implemented(report)

        except Exception as e:
            raise e

    def __select_mean_comsuption_per_distance(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_comsuption_per_distance")
        try:
            query = self.querys.select_mean_comsuption_per_distance(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean consumption per distance: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_comsuption_per_trip(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_comsuption_per_trip")
        try:
            query = self.querys.select_mean_comsuption_per_trip(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean consumption per trip: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_comsuption_per_working_hour(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_comsuption_per_working_time")
        try:
            query = self.querys.select_mean_comsuption_per_working_hour(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean consumption per working hour: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_comsuption_per_working_minute(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_comsuption_per_working_minute")
        try:
            query = self.querys.select_mean_comsuption_per_working_minute(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean consumption per working minute: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_distance(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_distance")
        try:
            query = self.querys.select_mean_distance(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean distance: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_number_of_trips(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_number_of_trips")
        try:
            query = self.querys.select_mean_number_of_trips(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_working_time(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | str]]:
        self.logger.debug("Starting __select_mean_working_time")
        try:
            query = self.querys.select_mean_working_time(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_time(report, car_ids)

            return self.return_time(results)

        except Exception as e:
            raise e

    def __select_mean_working_time_per_trip(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | str]]:
        self.logger.debug("Starting __select_mean_working_time_per_trip")
        try:
            query = self.querys.select_mean_working_time_per_trip(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_time(report, car_ids)

            return self.return_float_to_time(results)

        except Exception as e:
            raise e

    def __select_mean_value_received(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_value_received")
        try:
            query = self.querys.select_mean_value_received(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_value_received_per_comsuption(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_value_received_per_comsuption")
        try:
            query = self.querys.select_mean_value_received_per_comsuption(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_value_received_per_distance(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_value_received_per_distance")
        try:
            query = self.querys.select_mean_value_received_per_distance(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_value_received_per_trip(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_value_received_per_trip")
        try:
            query = self.querys.select_mean_value_received_per_trip(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_value_received_per_working_hour(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_value_received_per_working_hour")
        try:
            query = self.querys.select_mean_value_received_per_working_hour(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e

    def __select_mean_value_received_per_working_minute(
        self,
        db_session: scoped_session[Session],
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        report: str,
    ) -> Sequence[Mapping[str, uuid.UUID | float]]:
        self.logger.debug("Starting __select_mean_value_received_per_working_minute")
        try:
            query = self.querys.select_mean_value_received_per_working_minute(id_user, car_ids, date_, report)

            results: Sequence[RowMapping] = db_session.execute(query).mappings().all()

            self.logger.debug(f"Mean number of trips: {results}")

            if results is None:
                results = self.default_number(report, car_ids)

            return self.return_number(results)

        except Exception as e:
            raise e
