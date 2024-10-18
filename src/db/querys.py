import uuid
from typing import Any

from sqlalchemy import Delete, Insert, Select, Text, Update, delete, insert, select, text, update

from .Schemas import *


class Querys:
    def select_user_by_id(self, id_user: str) -> Select[tuple[UserSchema]]:
        return select(UserSchema).where(UserSchema.id_user == id_user)

    def select_user_by_cd_auth(self, cd_auth: str) -> Select[tuple[UserSchema]]:
        return select(UserSchema).where(UserSchema.cd_auth == cd_auth)

    def insert_user(self, new_user_data: dict[str, Any]) -> Insert[UserSchema]:
        return insert(UserSchema).values(**new_user_data)

    def delete_user(self, email: str) -> Delete[UserSchema]:
        return delete(UserSchema).where(UserSchema.email == email)

    def update_user(self, id_user: str, new_data: dict[str, Any]) -> Update[UserSchema]:
        return update(UserSchema).where(UserSchema.id_user == id_user).values(**new_data)
