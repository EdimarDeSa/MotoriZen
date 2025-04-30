from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user
from .utils.models import User


class TestFuelTypesSuccess:
    def test_get_all_fuel_types(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

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

    def test_get_specific_fuel_type(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

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
