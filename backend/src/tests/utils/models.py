from typing import TypedDict


class User(TypedDict):
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


class Data(TypedDict):
    users: list[User]
    vehicles: list[Vehicle]


class TokenData(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int
    scope: str
