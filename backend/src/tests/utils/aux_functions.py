from collections.abc import Generator
from uuid import UUID

from fastapi.responses import Response
from fastapi.testclient import TestClient
from sqlalchemy import insert, select, text
from sqlalchemy.orm import Session, scoped_session

from .constants import PASSWORD
from .data_base_aux import DBConnectionHandler, RegisterSchema, UserSchema, VehicleSchema
from .models import Register, TokenData, User, Vehicle


def get_csrf_token(client: TestClient) -> str:
    return client.get("/get-csrf-token").json()["data"]["csrf_token"]


def insert_user(client: TestClient, user: User) -> Response:
    csrf_token = get_csrf_token(client)
    response = client.post(
        "/users/new-user",
        headers={"X-CSRF-Token": csrf_token},
        json={"password": PASSWORD, **user},
    )
    return response


def login_user(client: TestClient, email: str) -> TokenData:
    csrf_token = get_csrf_token(client)
    response = client.post(
        "/token",
        headers={"X-CSRF-Token": csrf_token},
        data={
            "username": email,
            "password": PASSWORD,
            "grant_type": "password",
        },
    )
    return response.json()


def user_and_auth_generator(client: TestClient, users: list[User]) -> Generator[tuple[TokenData, User], None, None]:
    for user in users:
        insert_user(client, user)

    for user in users:
        token_data = login_user(client, user["email"])

        yield token_data, user


def select_user_ids(client: TestClient, db_session: scoped_session[Session], users: list[User]) -> dict[str, UUID]:
    user_emails = [user["email"] for user in users]
    user_ids = db_session.execute(
        select(UserSchema.email, UserSchema.id_user).where(UserSchema.email.in_(user_emails))
    ).all()
    return {email: id_user for email, id_user in user_ids}


def vehicles_already_exists(db_session: scoped_session[Session]) -> bool:
    return db_session.execute(text("SELECT COUNT(*) FROM tb_vehicle")).scalar() > 0


def insert_vehicles(
    db_session: scoped_session[Session],
    users: list[User],
    vehicles: list[Vehicle],
    user_cache: dict[str, UUID],
    qtd_vehicles_per_user: int,
) -> None:
    vehicle_gen = [
        {
            "cd_user": user_cache[user["email"]],
            **vehicle,
        }
        for user_index, user in enumerate(users)
        for vehicle in vehicles[(user_index * qtd_vehicles_per_user) : ((user_index + 1) * qtd_vehicles_per_user)]
    ]

    # Insert vehicles
    db_session.execute(insert(VehicleSchema).values(vehicle_gen))


def retrieve_vehicles_by_user(db_session: scoped_session[Session], user_id: UUID) -> list[Vehicle]:
    result = db_session.query(VehicleSchema).where(VehicleSchema.cd_user == user_id).all()
    return [v.as_dict() for v in result]


def retrieve_registers_by_user(db_session: scoped_session[Session], user_id: UUID) -> list[Register]:
    result = (
        db_session.query(RegisterSchema)
        .where(RegisterSchema.cd_user == user_id)
        .group_by(RegisterSchema.cd_vehicle, RegisterSchema.id_register)
        .all()
    )
    return result


def vehicles_generator(
    client: TestClient, users: list[User], vehicles: list[Vehicle], qtd_vehicles_per_user: int
) -> Generator[tuple[list[Vehicle], TokenData, User], None, None]:
    # Insert users
    for user in users:
        insert_user(client, user)

    # Create db session
    db_session = DBConnectionHandler.create_session(write=True)

    # Select user ids
    user_cache = select_user_ids(client, db_session, users)

    # Check if users already have vehicles
    if not vehicles_already_exists(db_session):
        insert_vehicles(db_session, users, vehicles, user_cache, qtd_vehicles_per_user)
        db_session.commit()

    for user in users:
        stored_vehicles = retrieve_vehicles_by_user(db_session, user_cache[user["email"]])

        token_data = login_user(client, user["email"])

        yield stored_vehicles, token_data, user

    db_session.close()


def registers_already_exists(db_session: scoped_session[Session]) -> bool:
    return db_session.execute(text("SELECT COUNT(*) FROM tb_register")).scalar() > 0


def insert_registers(
    db_session: scoped_session[Session],
    stored_vehicles: list[Vehicle],
    qtd_registers_per_vehicle: int,
    registers: list[Register],
) -> None:
    register_gen = [
        {
            "cd_user": vehicle.cd_user,
            "cd_vehicle": vehicle.id_vehicle,
            **register,
        }
        for vehicle_index, vehicle in enumerate(stored_vehicles)
        for register in registers[
            (vehicle_index * qtd_registers_per_vehicle) : ((vehicle_index + 1) * qtd_registers_per_vehicle)
        ]
    ]
    db_session.execute(insert(RegisterSchema).values(register_gen))


def regsiter_generator(
    client: TestClient,
    users: list[User],
    vehicles: list[Vehicle],
    registers: list[Register],
    qtd_vehicles_per_user: int,
    qtd_registers_per_vehicle: int,
) -> Generator[tuple[User, TokenData, list[VehicleSchema], list[RegisterSchema]], None, None]:
    # Insert users if they don't exist
    for user in users:
        insert_user(client, user)

    # Create db session
    db_session = DBConnectionHandler.create_session(write=True)

    # Select user ids
    user_cache = select_user_ids(client, db_session, users)

    # Check if users already have vehicles
    if not vehicles_already_exists(db_session):
        insert_vehicles(db_session, users, vehicles, user_cache, qtd_vehicles_per_user)

    stored_vehicles = db_session.query(VehicleSchema).all()

    if not registers_already_exists(db_session):
        insert_registers(db_session, stored_vehicles, qtd_registers_per_vehicle, registers)

    db_session.commit()

    for user in users:
        stored_vehicles = retrieve_vehicles_by_user(db_session, user_cache[user["email"]])
        stored_registers = retrieve_registers_by_user(db_session, user_cache[user["email"]])

        token_data = login_user(client, user["email"])

        yield user, token_data, stored_vehicles, stored_registers

    db_session.close()
