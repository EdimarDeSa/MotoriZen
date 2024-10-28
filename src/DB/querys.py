from typing import Any

from pydantic import BaseModel, InstanceOf
from sqlalchemy import Delete, Insert, Select, Text, Update, delete, func, insert, select, text, update

from DB.Models import CarQueryOptionsModel, RegisterQueryFiltersModel, RegisterQueryOptionsModel
from DB.Models.base_query_options_models import BaseQueryOptionsModel
from DB.Models.car_query_filters_model import CarQueryFiltersModel
from DB.Models.range_model import RangeModel
from DB.Schemas.base_schema import BaseSchema

from .Schemas import *


class Querys:
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

    ### Internal functions ###
    @classmethod
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

    @classmethod
    def _calculate_offset(cls, per_page: int | None, page: int | None) -> int:
        if per_page is None:
            per_page = 10

        if page is None:
            page = 1

        return per_page * (page - 1)

    @classmethod
    def _check_order_by(cls, table: type[BaseSchema], sort_by: str | None, sort_order: str | None) -> Any:
        if sort_by is None:
            sort_by = "id_" + table.__tablename__[3:]

        column = getattr(table, sort_by)

        if sort_order is None:
            sort_order = "asc"

        return column.asc() if sort_order == "asc" else column.desc()

    @classmethod
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

    @classmethod
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
