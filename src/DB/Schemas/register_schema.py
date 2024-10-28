import uuid
from datetime import date, datetime, time

from sqlalchemy import UUID, Date, DateTime, Float, ForeignKey, Integer, Time
from sqlalchemy.orm import MappedColumn, mapped_column

from DB.Schemas.base_schema import BaseSchema


class RegisterSchema(BaseSchema):
    __tablename__ = "tb_register"

    id_register: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    cd_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_user.id_user"), nullable=False, index=True)
    cd_car: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_car.id_car"), nullable=False, index=True)
    distance: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    working_time: MappedColumn[time] = mapped_column(Time(), nullable=False)
    mean_consuption: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    number_of_trips: MappedColumn[int] = mapped_column(Integer(), nullable=False, default=1)
    total_value: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    register_date: MappedColumn[date] = mapped_column(Date(), nullable=False, default=date.today, index=True)
    last_update: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    creation: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"DayResulltSchema({self.as_dict()!r})"

    def __str__(self) -> str:
        return (
            f"DayResulltSchema(id={self.id_resultado_do_dia!r}, cd_user={self.cd_user!r}, distance={self.distance!r}, "
            f"duration={self.duration!r}, total_value={self.total_value!r}, data_de_entrada={self.data_de_entrada!r})"
        )
