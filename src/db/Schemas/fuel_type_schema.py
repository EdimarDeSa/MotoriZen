from sqlalchemy import INTEGER, TIMESTAMP, String
from sqlalchemy.orm import MappedColumn, mapped_column

from db.Schemas.base_schema import BaseSchema


class FuelTypeSchema(BaseSchema):
    __tablename__ = "tb_fuel_type"

    id_fuel_type: MappedColumn[int] = mapped_column(INTEGER(), primary_key=True, autoincrement="auto")
    name: MappedColumn[str] = mapped_column(String(20), nullable=False, unique=True)
    updated_at: MappedColumn[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)
    created_at: MappedColumn[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)
    deleted_at: MappedColumn[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    def __str__(self) -> str:
        return f"{self.id_column} - {self.name}"
