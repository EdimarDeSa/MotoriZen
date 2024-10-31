import uuid
from datetime import date, time
from typing import Any, Sequence

from pydantic import BaseModel, InstanceOf
from sqlalchemy import Delete, Insert, Label, Select, Text, Update, delete, func, insert, select, text, true, update

from DB.Models import CarQueryFiltersModel, CarQueryOptionsModel, RegisterQueryFiltersModel, RegisterQueryOptionsModel
from DB.Models.base_query_options_models import BaseQueryOptionsModel
from DB.Models.range_model import RangeModel
from DB.Schemas.base_schema import BaseSchema
from Utils.constants import *

from .Schemas import *


class Querys:
    def insert_data(self, table: type[BaseSchema], data: dict[str, Any]) -> Insert:
        return insert(table).values(**data)

    ### User Querys ###
    def select_user_by_id(self, id_user: str) -> Select[tuple[UserSchema]]:
        return select(UserSchema).where(UserSchema.id_user == id_user).limit(1)

    def select_user_by_cd_auth(self, cd_auth: str) -> Select[tuple[UserSchema]]:
        return select(UserSchema).where(UserSchema.cd_auth == cd_auth).limit(1)

    def insert_user(self, new_user_data: dict[str, Any]) -> Insert:
        return insert(UserSchema).values(**new_user_data)

    def delete_user(self, email: str) -> Delete:
        return delete(UserSchema).where(UserSchema.email == email)

    def update_user(self, id_user: str, new_data: dict[str, Any]) -> Update:
        return update(UserSchema).where(UserSchema.id_user == id_user).values(**new_data)

    ### Car Querys ###
    def select_car_by_id(self, id_user: str, car_id: str) -> Select[tuple[CarSchema]]:
        return select(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == car_id).limit(1)

    def select_cars(
        self,
        id_user: str,
        query_filters: CarQueryFiltersModel,
        query_options: CarQueryOptionsModel,
    ) -> Select[tuple[CarSchema]]:
        return self._select_filtered_to_user(CarSchema, id_user, query_filters, query_options)

    def select_cars_count(self, id_user: str, query_filters: CarQueryFiltersModel) -> Select[tuple[int]]:
        filters = self._crete_data_filter(CarSchema, id_user, query_filters)

        return select(func.count(CarSchema.id_car)).where(*filters)

    def select_last_odometer(self, id_user: str, id_car: str) -> Select[tuple[float]]:
        return select(CarSchema.odometer).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car)

    def insert_car(self, car_data: dict[str, Any]) -> Insert:
        return insert(CarSchema).values(**car_data)

    def update_car(self, id_user: str, id_car: str, car_updates: dict[str, Any]) -> Update:
        return update(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car).values(**car_updates)

    def update_car_odometer(self, id_user: str, id_car: str, odometer: float) -> Update:
        return (
            update(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car).values(odometer=odometer)
        )

    def delete_car(self, id_user: str, id_car: str) -> Delete:
        return delete(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car)

    ### Brand Querys ###
    def select_brands(self) -> Select[tuple[BrandSchema]]:
        return select(BrandSchema)

    def select_brand(self, id_brand: int) -> Select[tuple[BrandSchema]]:
        return select(BrandSchema).where(BrandSchema.id_brand == id_brand)

    ### Register Querys ###
    def select_registers(
        self, id_user: str, query_filters: RegisterQueryFiltersModel, query_options: RegisterQueryOptionsModel
    ) -> Select[tuple[RegisterSchema]]:
        return self._select_filtered_to_user(RegisterSchema, id_user, query_filters, query_options)

    def select_register_by_id(self, id_user: str, id_register: str) -> Select[tuple[RegisterSchema]]:
        return select(RegisterSchema).where(
            RegisterSchema.cd_user == id_user, RegisterSchema.id_register == id_register
        )

    def insert_register(self, new_register_data: dict[str, Any]) -> Insert:
        return insert(RegisterSchema).values(**new_register_data)

    def update_register(self, id_user: str, id_register: str, updates: dict[str, Any]) -> Update:
        return (
            update(RegisterSchema)
            .where(RegisterSchema.cd_user == id_user, RegisterSchema.id_register == id_register)
            .values(**updates)
        )

    def delete_register(self, id_user: str, id_register: str) -> Delete:
        return delete(RegisterSchema).where(
            RegisterSchema.cd_user == id_user, RegisterSchema.id_register == id_register
        )

    ### Reports Querys ###
    def select_total_consumption(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.distance / RegisterSchema.mean_consuption).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_total_distance(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.distance).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_total_working_time(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, time]]:
        filter_ = func.sum(RegisterSchema.working_time).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_total_number_of_trips(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, int]]:
        filter_ = func.sum(RegisterSchema.number_of_trips).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_total_value_received(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.total_value).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    ### Means Querys ###
    def select_mean_comsuption_per_distance(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(RegisterSchema.distance / RegisterSchema.mean_consuption).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_comsuption_per_trip(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            (RegisterSchema.distance / RegisterSchema.mean_consuption) / RegisterSchema.number_of_trips
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_comsuption_per_working_hour(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            (RegisterSchema.distance / RegisterSchema.mean_consuption)
            / (func.extract("epoch", RegisterSchema.working_time) / 3600)
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_comsuption_per_working_minute(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            (RegisterSchema.distance / RegisterSchema.mean_consuption)
            / (func.extract("epoch", RegisterSchema.working_time) / 60)
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_distance(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(RegisterSchema.distance).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_number_of_trips(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(RegisterSchema.number_of_trips).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_working_time(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, time]]:
        filter_ = func.avg(RegisterSchema.working_time).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_working_time_per_trip(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            (func.extract("epoch", RegisterSchema.working_time) / 3600) / RegisterSchema.number_of_trips
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_value_received(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(RegisterSchema.total_value).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_value_received_per_comsuption(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            RegisterSchema.total_value / (RegisterSchema.distance / RegisterSchema.mean_consuption)
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_value_received_per_distance(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(RegisterSchema.total_value / RegisterSchema.distance).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_value_received_per_trip(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(RegisterSchema.total_value / RegisterSchema.number_of_trips).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_value_received_per_working_hour(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            RegisterSchema.total_value / (func.extract("epoch", RegisterSchema.working_time) / 3600)
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    def select_mean_value_received_per_working_minute(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.avg(
            RegisterSchema.total_value / (func.extract("epoch", RegisterSchema.working_time) / 60)
        ).label(report)

        return self._select_report(id_user, car_ids, date_, filter_)

    ### Daily report querys ###
    def select_comsuption_per_day(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.distance / RegisterSchema.mean_consuption).label(report)

        return self._select_periodcaly_report(id_user, car_ids, date_, "day", filter_)

    def select_daily_distance(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.distance).label(report)

        return self._select_periodcaly_report(id_user, car_ids, date_, "day", filter_)

    def select_daily_working_time(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.working_time).label(report)

        return self._select_periodcaly_report(id_user, car_ids, date_, "day", filter_)

    def select_daily_number_of_trips(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.number_of_trips).label(report)

        return self._select_periodcaly_report(id_user, car_ids, date_, "day", filter_)

    def select_daily_value_received(
        self, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report: str
    ) -> Select[tuple[uuid.UUID, float]]:
        filter_ = func.sum(RegisterSchema.total_value).label(report)

        return self._select_periodcaly_report(id_user, car_ids, date_, "day", filter_)

    ### Internal functions ###
    def _select_filtered_to_user(
        cls,
        table: type[BaseSchema],
        id_user: str,
        query_filters: InstanceOf[BaseModel],
        query_options: InstanceOf[BaseQueryOptionsModel],
    ) -> Select[tuple[BaseSchema]]:
        offset = cls._calculate_offset(query_options.per_page, query_options.page)

        order_by = cls._check_order_by(table, query_options.sort_by, query_options.sort_order)

        filters = cls._crete_data_filter(table, id_user, query_filters)

        return select(table).where(*filters).offset(offset).limit(query_options.per_page).order_by(order_by)

    def _calculate_offset(cls, per_page: int | None, page: int | None) -> int:
        if per_page is None:
            per_page = 10

        if page is None:
            page = 1

        return per_page * (page - 1)

    def _check_order_by(cls, table: type[BaseSchema], sort_by: str | None, sort_order: str | None) -> Any:
        if sort_by is None:
            sort_by = "id_" + table.__tablename__[3:]

        column = getattr(table, sort_by)

        if sort_order is None:
            sort_order = "asc"

        return column.asc() if sort_order == "asc" else column.desc()

    def _crete_data_filter(
        cls, table: type[BaseSchema], id_user: str, query_filters: InstanceOf[BaseModel]
    ) -> list[Any]:
        filters = [table.cd_user == id_user]

        if not query_filters.model_fields_set:
            return filters

        for key in query_filters.model_fields_set:
            if not hasattr(table, key):
                continue

            value = getattr(query_filters, key)

            if isinstance(value, RangeModel):
                table_column = getattr(table, key)

                filters.append(table_column >= value.start)

                if value.end is not None:
                    filters.append(table_column <= value.end)

                continue

            filters.append(getattr(table, key) == value)

        return filters

    def count_total_results(
        cls, table: type[BaseSchema], id_user: str, query_filters: InstanceOf[BaseModel]
    ) -> Select[tuple[int]]:
        """
        Count total results of a query for a given user and filters

        Args:

            table (type[BaseSchema]): The table schema to query from
            id_user (str): The user id
            query_filters (InstanceOf[BaseModel]): The query filters to apply

        Returns:

            Select[tuple[int]]: The total results count
        """
        filters = cls._crete_data_filter(table, id_user, query_filters)

        id_column = getattr(table, "id_" + table.__tablename__[3:])

        return select(func.count(id_column)).where(*filters)

    def _select_report(
        cls, id_user: str, car_ids: Sequence[uuid.UUID], date_: RangeModel[date], report_query: Label[Any]
    ) -> Select[tuple[uuid.UUID, Any]]:
        return (
            select(RegisterSchema.cd_car.label(CAR_LABEL), report_query)
            .where(
                RegisterSchema.cd_user == id_user,
                RegisterSchema.cd_car.in_(car_ids) if car_ids else true(),
                RegisterSchema.register_date.between(date_.start, date_.end),
            )
            .group_by(RegisterSchema.cd_car)
        )

    def _select_periodcaly_report(
        self,
        id_user: str,
        car_ids: Sequence[uuid.UUID],
        date_: RangeModel[date],
        periode: str,
        report_query: Label[Any],
    ) -> Select[tuple[uuid.UUID, Any]]:
        return (
            select(
                RegisterSchema.cd_car.label(CAR_LABEL),
                func.date_trunc(periode, RegisterSchema.register_date).label(REGISTER_DATE),
                report_query,
            )
            .where(
                RegisterSchema.cd_user == id_user,
                RegisterSchema.cd_car.in_(car_ids) if car_ids else true(),
                RegisterSchema.register_date.between(date_.start, date_.end),
            )
            .group_by(RegisterSchema.cd_car, RegisterSchema.register_date)
        )
