from urllib import response

from starlette.testclient import TestClient

from .conftest import insert_user, login_user, logout_user
from .utils.models import TokenData, User


class TestFuelTypesSuccess:
    def test_get_all_fuel_types(self, client: TestClient, users: list[User]) -> None:
        # Given
        user = users[0]
        insert_user(client, user)
        response = login_user(client, user)
        token_data: TokenData = response.json()

        # When
        response = client.post(
            "/fuel-types/get-fuel-types",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

        rc = response.json()["rc"]
        fuel_types = response.json()["data"]

        # Then
        assert response.status_code == 200
        assert rc == 0
        assert len(fuel_types) > 0

        logout_user(client, token_data["access_token"])

    def test_get_specific_fuel_type(self, client: TestClient, users: list[User]) -> None:
        # Given
        user = users[0]
        insert_user(client, user)
        response = login_user(client, user)
        token_data: TokenData = response.json()

        # When
        response = client.get(
            "/fuel-types/get-fuel-type/1",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

        rc = response.json()["rc"]
        fuel_type = response.json()["data"]

        # Then
        assert response.status_code == 200
        assert rc == 0
        assert fuel_type["id_fuel_type"] == 1
        assert fuel_type["name"] == "Alcohol"

        logout_user(client, token_data["access_token"])
