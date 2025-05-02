from collections.abc import Generator
from datetime import datetime
from functools import wraps
from uuid import UUID, uuid4

from fastapi.responses import Response
from fastapi.testclient import TestClient
from sqlalchemy import Result, insert, select, text

from .constants import PASSWORD
from .data_base_aux import DBConnectionHandler, RegisterSchema, UserSchema, VehicleSchema
from .models import TokenData, User, Vehicle


def print_progress(*args) -> None:
    formatted_args = [str(arg).center(25) for arg in args]

    print(
        "Progress:".ljust(12),
        *formatted_args,
        sep=" │ ",
        end="\r",
    )


def with_progress(description: str = ""):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            initial_time = datetime.now()
            # Imprime uma linha vazia antes do teste
            print()

            # Se houver descrição, imprime
            if description:
                print(f"🚀 {description}")

            try:
                result = test_func(*args, **kwargs)
            finally:
                final_time = datetime.now()
                total_time = (final_time - initial_time).total_seconds()
                print()
                print(f"Time: {total_time:.2f}s")

            return result

        return wrapper

    return decorator


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


def get_user_data(client: TestClient, access_token: str) -> User:
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return response.json()["data"]


def delete_user(client: TestClient, access_token: str) -> None:
    client.delete(
        "/users/delete-user",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_and_athenticate_user(
    client: TestClient, users: list[User], delete_after: bool = True
) -> Generator[tuple[TokenData, User], None, None]:
    for user in users:
        insert_user(client, user)

    for user in users:
        token_data = login_user(client, user["email"])

        yield token_data, user

        if not delete_after:
            continue

        delete_user(client, token_data["access_token"])


def create_vehicles(
    client: TestClient, users: list[User], vehicles: list[Vehicle], qtd_vehicles_per_user: int
) -> Generator[tuple[list[Vehicle], TokenData, User], None, None]:
    # Insert users
    for user in users:
        insert_user(client, user)

    # Create db session
    db_session = DBConnectionHandler.create_session(write=True)

    # Select user ids
    user_emails = [user["email"] for user in users]
    user_ids = db_session.execute(
        select(UserSchema.email, UserSchema.id_user).where(UserSchema.email.in_(user_emails))
    ).all()
    user_cache = {email: id_user for email, id_user in user_ids}

    # Prepare vehicles to insert
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
    db_session.commit()

    for user in users:
        token_data = login_user(client, user["email"])

        result = db_session.query(VehicleSchema).where(VehicleSchema.cd_user == user_cache[user["email"]]).all()
        stored_vehicles = [v.as_dict() for v in result]

        yield stored_vehicles, token_data, user

        delete_user(client, token_data["access_token"])

    db_session.close()
