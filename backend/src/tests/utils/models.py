from datetime import date, time
from typing import Optional, TypedDict

from .data_base_aux import RegisterSchema, UserSchema, VehicleSchema


class User(TypedDict):
    id_user: str | None
    first_name: str
    last_name: str
    email: str
    birthdate: str


class Vehicle(TypedDict):
    cd_brand: int
    renavam: str
    model: str
    year: int
    color: str
    fuel_capacity: int
    cd_fuel_type: int
    license_plate: str
    odometer: float
    is_active: bool


class Register(TypedDict):
    cd_vehicle: str
    number_of_trips: int
    distance: Optional[float]
    odometer: Optional[float]
    working_time: time
    mean_consuption: float
    total_value: float
    register_date: date


class Data(TypedDict):
    users: list[User]
    vehicles: list[Vehicle]
    registers: list[Register]


class TokenData(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int
    scope: str


class StaticRegisters(TypedDict):
    day: list[Register]
    week: list[Register]
    month: list[Register]
    year: list[Register]


class StaticData(TypedDict):
    users: list[User]
    vehicles: list[Vehicle]
    registers: StaticRegisters


class StaticRegistersSchemas(TypedDict):
    day: dict[
        "registers" : list[RegisterSchema],
        "results" : list[Register],
    ]
    week: list[Register]
    month: list[Register]
    year: list[Register]


class StaticUserData(TypedDict):
    token_data: TokenData
    user: UserSchema
    vehicles: list[VehicleSchema]
    registers: StaticRegistersSchemas
