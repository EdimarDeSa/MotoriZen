from typing import Any

from sqlalchemy.orm import DeclarativeBase, declarative_base

Base: DeclarativeBase = declarative_base()


class BaseSchema(Base):
    __abstract__ = True
    __table_args__ = {"schema": "motorizen"}

    def as_dict(self, *, exclude_none: bool = False) -> dict[str, Any]:
        if exclude_none:
            return {c.name: getattr(self, c.name) for c in self.__table__.c if getattr(self, c.name) is not None}
        return {c.name: getattr(self, c.name) for c in self.__table__.c}
