from curses import meta
from typing import Any
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, declarative_base

from Utils.custom_primitive_types import TableDict

Base: DeclarativeBase = declarative_base()


class BaseSchema(Base):  # type: ignore
    __abstract__ = True
    __table_args__ = {"schema": "motorizen"}

    def as_dict(self, *, exclude_none: bool = False) -> TableDict:
        """
        Returns a dictionary representation of the schema

        Args:
            exclude_none (bool, optional): If True, exclude columns with None values. Defaults to False.

        Returns:
            TableDict: Dictionary representation of the schema with optional filtering

        Example:
            >>> from db.Schemas.user_schema import UserSchema
            >>> user_schema = UserSchema()
            >>> user_schema.as_dict()
            {'id_user': None, 'first_name': 'Eduard', 'last_name': 'Hernandez', 'email': 'eduard.hernandez@example.com', 'birthdate': '1990-01-01', 'cd_auth': None, 'is_active': None, 'last_update': None, 'creation': None}
            >>> user_schema.as_dict(exclude_none=True)
            {'first_name': 'Eduard', 'last_name': 'Hernandez', 'email': 'eduard.hernandez@example.com', 'birthdate': '1990-01-01'}
        """
        if exclude_none:
            return {c.name: getattr(self, c.name) for c in self.__table__.c if getattr(self, c.name) is not None}
        return {c.name: getattr(self, c.name) for c in self.__table__.c}

    @classmethod
    def fields(cls) -> tuple[str]:
        """
        Returns a tuple of fields in the schema

        Returns:
            fields (tuple[str]): Tuple of fields in the schema
        """
        return tuple(c.name for c in cls.__table__.c)

    @classmethod
    def id_column(cls) -> int | UUID:
        return getattr(cls, "id_" + cls.__tablename__[3:])

    def __repr__(self) -> str:
        return f"{self.__class__.name}({self.as_dict()!r})"

    def __str__(self) -> str:
        if hasattr(self, "name"):
            return f"{self.id_column} - {self.name}"
        return f"{self.id_column()} - {self.fields()}"
