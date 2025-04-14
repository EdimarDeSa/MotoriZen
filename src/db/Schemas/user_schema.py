import uuid
from datetime import date, datetime

from sqlalchemy import UUID, Boolean, Date, DateTime, String
from sqlalchemy.orm import MappedColumn, mapped_column

from db.Schemas.base_schema import BaseSchema


class UserSchema(BaseSchema):
    __tablename__ = "tb_user"

    id_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    first_name: MappedColumn[str] = mapped_column(String(50), nullable=False)
    last_name: MappedColumn[str] = mapped_column(String(100), nullable=False)
    email: MappedColumn[str] = mapped_column(String(255), nullable=False, unique=True)
    birthdate: MappedColumn[date] = mapped_column(Date(), nullable=False)
    cd_auth: MappedColumn[uuid.UUID] = mapped_column(UUID(), nullable=False)
    is_active: MappedColumn[bool] = mapped_column(Boolean(), nullable=False, default=True)
    updated_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.__class__.name}(id={self.id_user!r}, name={self.full_name!r}, email={self.email!r})"
