import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, Float, ForeignKey
from sqlalchemy.orm import MappedColumn, mapped_column

from db.Schemas.base_schema import BaseSchema


class CarSchema(BaseSchema):
    __tablename__ = "tb_car"

    id_car: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    cd_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_user.id_user"), nullable=False, index=True)
    odometer: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    last_update: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    creation: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"CarSchema({self.as_dict()!r})"

    def __str__(self) -> str:
        return f"CarSchema(id={self.id_car!r}, cd_user={self.cd_user!r}, odometer={self.odometer!r})"
