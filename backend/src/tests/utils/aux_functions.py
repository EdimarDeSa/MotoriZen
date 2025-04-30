from collections.abc import Generator

from fastapi.responses import Response
from fastapi.testclient import TestClient

from .constants import PASSWORD
from .models import TokenData, User, Vehicle


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


def login_user(client: TestClient, user: User) -> TokenData:
    csrf_token = get_csrf_token(client)
    response = client.post(
        "/token",
        headers={"X-CSRF-Token": csrf_token},
        data={
            "username": user["email"],
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


def create_and_athenticate_user(client: TestClient, users: list[User]) -> Generator[tuple[TokenData, User], None, None]:
    for user in users:
        insert_user(client, user)
        token_data = login_user(client, user)
        user_data = get_user_data(client, token_data["access_token"])

        yield token_data, user_data

        delete_user(client, token_data["access_token"])


def create_vehicles(
    client: TestClient, users: list[User], vehicles: list[Vehicle], qtd_vehicles_per_user: int
) -> Generator[tuple[list[Vehicle], TokenData, User], None, None]:
    vehicle_offset = 0
    for token_data, user in create_and_athenticate_user(client, users):
        user_vehicles_raw = vehicles[vehicle_offset : vehicle_offset + qtd_vehicles_per_user]

        user_vehicles = [
            client.post(
                "/vehicles/new-vehicle",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                json=vehicle,
            ).json()["data"]
            for vehicle in user_vehicles_raw
        ]

        yield user_vehicles, token_data, user
