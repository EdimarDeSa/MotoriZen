import uuid

from sqlalchemy import INTEGER, String
from sqlalchemy.orm import MappedColumn, mapped_column

from DB.Schemas.base_schema import BaseSchema


class FuelTypeSchema(BaseSchema):
    __tablename__ = "tb_fuel_type"

    id_fuel_type: MappedColumn[int] = mapped_column(INTEGER(), primary_key=True, autoincrement="auto")
    name: MappedColumn[str] = mapped_column(String(20), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"{self.__class__.name}({self.as_dict()!r})"

    def __str__(self) -> str:
        return f"{self.id_column} - {self.name}"
