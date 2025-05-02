import os
import uuid
from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import UUID, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Time, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedColumn,
    Session,
    declarative_base,
    mapped_column,
    scoped_session,
    sessionmaker,
)


def get_db_url() -> str:
    db_dialect: str = os.getenv("DB_DIALECT")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_ip: str = os.getenv("DB_IP")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_MOTORIZEN")

    return f"{db_dialect}://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}"


class DBConnectionHandler:
    @staticmethod
    def create_session(*, db_url: Optional[str] = None, write: bool = False) -> scoped_session[Session]:
        if db_url is None:
            db_url = get_db_url()

        engine: Engine = create_engine(
            db_url, pool_size=250, max_overflow=50, pool_use_lifo=True, pool_pre_ping=True, pool_recycle=300
        )

        if write:
            return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base: DeclarativeBase = declarative_base()


class BaseSchema(Base):  # type: ignore
    __abstract__ = True
    __table_args__ = {"schema": os.getenv("DB_MOTORIZEN_SCHEMA")}


class UserSchema(BaseSchema):
    __tablename__ = "tb_user"

    id_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    email: MappedColumn[str] = mapped_column(String(255), nullable=False, unique=True)


class VehicleSchema(BaseSchema):
    __tablename__ = "tb_vehicle"

    id_vehicle: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    cd_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_user.id_user"), nullable=False, index=True)
    cd_brand: MappedColumn[int] = mapped_column(Integer(), nullable=False, index=True)
    renavam: MappedColumn[str] = mapped_column(String(11), nullable=True, unique=True)
    model: MappedColumn[str] = mapped_column(String(100), nullable=False)
    year: MappedColumn[int] = mapped_column(Integer(), nullable=False)
    color: MappedColumn[str] = mapped_column(String(25), nullable=False)
    license_plate: MappedColumn[str] = mapped_column(String(10), nullable=False, unique=True)
    cd_fuel_type: MappedColumn[int] = mapped_column(Integer(), nullable=False, index=False)
    fuel_capacity: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    odometer: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    is_active: MappedColumn[bool] = mapped_column(Boolean(), nullable=False, default=True)
    updated_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def __str__(self) -> str:
        return f"{self.__class__.name}(id={self.id_vehicle!r}, cd_user={self.cd_user!r}, odometer={self.odometer!r})"

    def as_dict(self) -> dict:
        return {
            "id_vehicle": str(self.id_vehicle),
            "cd_brand": self.cd_brand,
            "renavam": self.renavam,
            "model": self.model,
            "year": self.year,
            "color": self.color,
            "license_plate": self.license_plate,
            "cd_fuel_type": self.cd_fuel_type,
            "fuel_capacity": self.fuel_capacity,
            "odometer": self.odometer,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat(),
            "created_at": self.created_at.isoformat(),
        }


class RegisterSchema(BaseSchema):
    __tablename__ = "tb_register"

    id_register: MappedColumn[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    cd_user: MappedColumn[uuid.UUID] = mapped_column(UUID(), ForeignKey("tb_user.id_user"), nullable=False, index=True)
    cd_vehicle: MappedColumn[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("tb_vehicle.id_vehicle"), nullable=False, index=True
    )
    distance: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    working_time: MappedColumn[time] = mapped_column(Time(), nullable=False)
    mean_consuption: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    number_of_trips: MappedColumn[int] = mapped_column(Integer(), nullable=False, default=1)
    total_value: MappedColumn[float] = mapped_column(Float(precision=2), nullable=False, default=0.0)
    register_date: MappedColumn[date] = mapped_column(Date(), nullable=False, default=date.today, index=True)
    updated_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
