import json
from pathlib import Path

from fastapi.responses import Response
from pytest import fixture
from starlette.testclient import TestClient

from .utils.constants import PASSWORD
from .utils.models import Data, User, Vehicle


@fixture(scope="session")
def client() -> TestClient:
    from main import app

    return TestClient(app)


@fixture(scope="module")
def _data() -> Data:
    data_file: Path = Path(__file__).resolve().parent / "data.json"
    with open(data_file, "r") as json_file:
        _data: Data = json.load(json_file)

        if _data is None:
            raise ValueError("Invalid data file")

    return _data


@fixture(scope="module")
def users(_data: Data) -> list[User]:
    return _data["users"]


@fixture(scope="module")
def vehicles(_data: Data) -> list[Vehicle]:
    return _data["vehicles"]


def get_csrf_token(client: TestClient) -> str:
    return client.get("/get-csrf-token").json()["data"]["csrf_token"]


def login_user(client: TestClient, user: User) -> Response:
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
    return response


def create_user(client: TestClient, user: User) -> Response:
    csrf_token = get_csrf_token(client)
    response = client.post(
        "/users/new-user",
        headers={"X-CSRF-Token": csrf_token},
        json={"password": PASSWORD, **user},
    )
    return response


def logout_user(client: TestClient, access_token: str) -> Response:
    response = client.get(
        "/token/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return response
