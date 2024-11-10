import uuid
from datetime import date, datetime

from sqlalchemy import UUID, Boolean, Date, DateTime, String
from sqlalchemy.orm import MappedColumn, mapped_column

from DB.Schemas.base_schema import BaseSchema


class UserSchema(BaseSchema):
    __tablename__ = "tb_user"

    id_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    first_name: MappedColumn[str] = mapped_column(String(50), nullable=False)
    last_name: MappedColumn[str] = mapped_column(String(100), nullable=False)
    email: MappedColumn[str] = mapped_column(String(255), nullable=False, unique=True)
    birthdate: MappedColumn[date] = mapped_column(Date(), nullable=False)
    cd_auth: MappedColumn[uuid.UUID] = mapped_column(UUID(), nullable=False)
    is_active: MappedColumn[bool] = mapped_column(Boolean(), nullable=False, default=True)
    last_update: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    creation: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"User(id={self.id_user!r}, name={self.name!r}, email={self.email!r})"

    def __str__(self) -> str:
        return f"User(id={self.id_user!r}, name={self.name!r}, email={self.email!r})"
