from typing import Any

from sqlalchemy import Delete, Insert, Select, Text, Update, delete, func, insert, select, text, update

from db.Models.car_model import CarQueryOptions
from db.Schemas.base_schema import BaseSchema
from db.Schemas.brand_schema import BrandSchema

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
        query_params_dict: dict[str, Any],
        query_options: CarQueryOptions,
    ) -> Select[tuple[CarSchema]]:
        offset = self._calculate_offset(query_options.per_page, query_options.page)

        order_by = self._check_order_by(CarSchema, query_options.sort_by, query_options.sort_order)

        filters = self._crete_user_data_filter(CarSchema, id_user, query_params_dict)

        return select(CarSchema).where(*filters).offset(offset).limit(query_options.per_page).order_by(order_by)

    def select_cars_count(self, id_user: str, query_params_dict: dict[str, Any]) -> Select[tuple[int]]:
        filters = [CarSchema.cd_user == id_user]
        for key, value in query_params_dict.items():
            if hasattr(CarSchema, key):
                filters.append(getattr(CarSchema, key) == value)

        return select(func.count(CarSchema.id_car)).where(*filters)

    def insert_car(self, car_data: dict[str, Any]) -> Insert:
        return insert(CarSchema).values(**car_data)

    def update_car(self, id_user: str, id_car: str, car_updates: dict[str, Any]) -> Update:
        return update(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car).values(**car_updates)

    def delete_car(self, id_user: str, id_car: str) -> Delete:
        return delete(CarSchema).where(CarSchema.cd_user == id_user, CarSchema.id_car == id_car)

    ### Brand Querys ###
    def select_brands(self) -> Select[tuple[BrandSchema]]:
        return select(BrandSchema)

    def select_brand(self, id_brand: int) -> Select[tuple[BrandSchema]]:
        return select(BrandSchema).where(BrandSchema.id_brand == id_brand)

    ### Internal functions ###
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
    def _crete_user_data_filter(cls, table: type[BaseSchema], id_user: str, fields: dict[str, Any]) -> list[Any]:
        filters = [table.cd_user == id_user]

        if not fields:
            return filters

        for key, value in fields.items():
            if hasattr(table, key):
                filters.append(getattr(table, key) == value)

        return filters
