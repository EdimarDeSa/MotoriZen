from urllib import response

from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user
from .utils.models import User


class TestBrandsSuccess:
    def test_get_all_brands(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

            # When
            response = client.post(
                "/brands/get-brands",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            rc = response.json()["rc"]
            brands = response.json()["data"]

            # Then
            assert response.status_code == 200
            assert rc == 0
            assert len(brands) > 0

    def test_get_specific_brand(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, user in create_and_athenticate_user(client, users):

            # When
            response = client.get(
                "/brands/get-brand/1",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            rc = response.json()["rc"]
            brand = response.json()["data"]

            # Then
            assert response.status_code == 200
            assert rc == 0
            assert brand["id_brand"] == 1
            assert brand["name"] == "Acura"
