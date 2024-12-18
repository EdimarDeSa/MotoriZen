import json
from pathlib import Path
from typing import Any, TypedDict

from faker import Faker
from pytest import fixture
from starlette.testclient import TestClient

from DB.Models.token_model import TokenModel

PASSWORD: str = "P@s5W0rd"


class User(TypedDict):
    first_name: str
    last_name: str
    email: str
    birthdate: str
    password: str


class Car(TypedDict):
    cd_brand: int
    renavam: str
    model: str
    year: int
    color: str
    license_plate: str
    odometer: float


class Data(TypedDict):
    users: list[User]
    cars: list[Car]


@fixture(scope="session")
def client() -> TestClient:
    from main import app

    return TestClient(app)


@fixture(scope="session")
def fake_data() -> Faker:
    return Faker("pt_br")


@fixture(scope="session")
def _data() -> Data:
    data_file: Path = Path(__file__).resolve().parent / "data.json"
    with open(data_file, "r") as json_file:
        _data: Data = json.load(json_file)

        if _data is None:
            raise ValueError("Invalid data file")

    return _data


@fixture(scope="session")
def users(_data: Data) -> list[User]:
    return _data["users"]


@fixture(scope="session")
def cars(_data: Data) -> list[Car]:
    return _data["cars"]


def token(client: TestClient, user: User) -> TokenModel:
    user_login = {
        "username": user["email"],
        "password": user["password"],
    }
    response = client.post("/token", data=user_login)
    return TokenModel.model_validate(response.json())


# def test_create_users_success(client: TestClient, users: list[User]) -> None:
#     for user in users:
#         user_data = {"password": PASSWORD, **user}

#         response = client.post("/users/new-user", json=user_data)

#         assert response.status_code == 201


def test_get_access_token_success(
    client: TestClient,
    users: list[User],
) -> None:

    # Given
    user = users[0]

    _token: TokenModel = token(client, user)
    header = {"Authorization": f"Bearer {_token.access_token}"}

    # Act
    me = client.get("/users/me", headers=header)
    me_rc = me.json()["rc"]
    me_data = me.json()["data"]

    # Assert
    assert me_rc == 0
    assert me_data["first_name"] == user["first_name"]


def test_logout_success(
    client: TestClient,
    users: list[User],
) -> None:

    # Given
    user = users[0]

    _token: TokenModel = token(client, user)
    header = {"Authorization": f"Bearer {_token.access_token}"}

    # Act
    me = client.get("/logout", headers=header)

    # Assert
    assert me.status_code == 204


def test_delete_account_success(client: TestClient, users: list[User]) -> None:

    # Given
    user = users[0]

    _token: TokenModel = token(client, user)
    header = {"Authorization": f"Bearer {_token.access_token}"}

    # Act
    me = client.delete("/users/delete-user", headers=header)

    # Assert
    assert me.status_code == 204
