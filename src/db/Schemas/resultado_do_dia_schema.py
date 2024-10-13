import uuid
from datetime import date, datetime

from sqlalchemy import UUID, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import MappedColumn, mapped_column

from db.Schemas.base_schema import BaseSchema


class ResultadoDoDiaSchema(BaseSchema):
    __tablename__ = "tb_resultado_do_dia"

    id_resultado_do_dia: MappedColumn[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, default=uuid.uuid4, nullable=False
    )
    cd_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_user.id_user"), nullable=False)
    distance: MappedColumn[float] = mapped_column(Float(), nullable=False, default=0.0)
    duration: MappedColumn[float] = mapped_column(Float(), nullable=False, default=0.0)
    total_value: MappedColumn[float] = mapped_column(Float(), nullable=False, default=0.0)
    data_de_entrada: MappedColumn[date] = mapped_column(Date(), nullable=False, default=date.today)
    last_update: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    creation: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return (
            f"ResultadoDoDia(id={self.id_resultado_do_dia!r}, cd_user={self.cd_user!r}, distance={self.distance!r}, "
            f"duration={self.duration!r}, total_value={self.total_value!r}, data_de_entrada={self.data_de_entrada!r})"
        )

    def __str__(self) -> str:
        return (
            f"ResultadoDoDia(id={self.id_resultado_do_dia!r}, cd_user={self.cd_user!r}, distance={self.distance!r}, "
            f"duration={self.duration!r}, total_value={self.total_value!r}, data_de_entrada={self.data_de_entrada!r})"
        )
