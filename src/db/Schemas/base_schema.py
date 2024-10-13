from sqlalchemy.orm import DeclarativeBase, declarative_base

base: DeclarativeBase = declarative_base()


class BaseSchema(base):
    __abstract__ = True
    __table_args__ = {"schema": "motorizen"}
