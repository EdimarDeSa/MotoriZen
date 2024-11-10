from typing import Any

from pydantic import BaseModel, InstanceOf
from sqlalchemy import Delete, Insert, Select, Update, delete, func, insert, select, update

from DB.Models.base_query_options_models import BaseQueryOptionsModel
from DB.Querys.base_query_manager import BaseQueryManager
from DB.Schemas.base_schema import BaseSchema
from Utils.custom_primitive_types import Table, TableDict

from ..Schemas import UserSchema


class UserQueryManager(BaseQueryManager):
    def select_user_by_id(self, id_user: str) -> Select[tuple[UserSchema]]:
        return select(UserSchema).where(UserSchema.id_user == id_user).limit(1)

    def select_user_by_cd_auth(self, cd_auth: str) -> Select[tuple[UserSchema]]:
        return select(UserSchema).where(UserSchema.cd_auth == cd_auth).limit(1)

    def delete_user(self, email: str) -> Delete:
        return delete(UserSchema).where(UserSchema.email == email)

    def update_user(self, id_user: str, new_data: dict[str, Any]) -> Update:
        return update(UserSchema).where(UserSchema.id_user == id_user).values(**new_data)

    def select_user_data_by_id(self, table: Table, id_user: str, id_data: str) -> Select[tuple[BaseSchema]]:
        return select(table).where(table.cd_user == id_user, table.id_column() == id_data).limit(1)

    def insert_data(self, table: Table, data: TableDict) -> Insert:
        return insert(table).values(**data)

    def update_user_data(self, table: Table, id_user: str, id_data: str, data: TableDict) -> Update:
        return update(table).where(table.cd_user == id_user, table.id_column() == id_data).values(**data)

    def delete_user_data(self, table: Table, id_user: str, id_data: str) -> Delete:
        return delete(table).where(table.cd_user == id_user, table.id_column() == id_data)

    def select_filtered_user_data(
        cls,
        table: Table,
        id_user: str,
        query_filters: InstanceOf[BaseModel],
        query_options: InstanceOf[BaseQueryOptionsModel],
    ) -> Select[tuple[BaseSchema]]:
        offset = cls.calculate_offset(query_options.per_page, query_options.page)

        order_by = cls.check_order_by(table, query_options.sort_by, query_options.sort_order)

        filters = cls.crete_data_filter(table, id_user, query_filters)

        return select(table).where(*filters).offset(offset).limit(query_options.per_page).order_by(order_by)

    def count_total_results(
        cls, table: Table, id_user: str, query_filters: InstanceOf[BaseModel]
    ) -> Select[tuple[int]]:
        """
        Count total results of a query for a given user and filters

        Args:

            table (Table): The table schema to query from
            id_user (str): The user id
            query_filters (InstanceOf[BaseModel]): The query filters to apply

        Returns:

            Select[tuple[int]]: The total results count
        """
        filters = cls.crete_data_filter(table, id_user, query_filters)

        return select(func.count(table.id_column())).where(*filters)
