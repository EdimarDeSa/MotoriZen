import uuid
from calendar import c
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import MappedColumn, mapped_column

from DB.Schemas.base_schema import BaseSchema


class CarSchema(BaseSchema):
    __tablename__ = "tb_car"

    id_car: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    cd_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_user.id_user"), nullable=False, index=True)
    cd_brand: MappedColumn[int] = mapped_column(Integer(), ForeignKey("tb_brand.id_brand"), nullable=False, index=True)
    renavam: MappedColumn[str] = mapped_column(String(11), nullable=True, unique=True)
    model: MappedColumn[str] = mapped_column(String(100), nullable=False)
    year: MappedColumn[int] = mapped_column(Integer(), nullable=False)
    color: MappedColumn[str] = mapped_column(String(25), nullable=False)
    license_plate: MappedColumn[str] = mapped_column(String(10), nullable=False, unique=True)
    cd_fuel_type: MappedColumn[int] = mapped_column(
        Integer(), ForeignKey("tb_fuel_type.id_fuel_type"), nullable=False, index=False
    )
    fuel_capacity: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    odometer: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    is_active: MappedColumn[bool] = mapped_column(Boolean(), nullable=False, default=True)
    last_update: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    creation: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"CarSchema({self.as_dict()!r})"

    def __str__(self) -> str:
        return f"CarSchema(id={self.id_car!r}, cd_user={self.cd_user!r}, odometer={self.odometer!r})"
