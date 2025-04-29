from collections.abc import Generator

from fastapi.responses import Response
from fastapi.testclient import TestClient

from .constants import PASSWORD
from .models import TokenData, User


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


def logout_user(client: TestClient, access_token: str) -> Response:
    response = client.get(
        "/token/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return response


def create_and_athenticate_user(client: TestClient, users: list[User]) -> Generator[tuple[TokenData, User], None, None]:
    for user in users:
        insert_user(client, user)
        token_data = login_user(client, user)

        yield token_data, user

        logout_user(client, token_data["access_token"])
