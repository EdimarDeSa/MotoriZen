from urllib import response

from starlette.testclient import TestClient

from .conftest import insert_user, login_user, logout_user
from .utils.models import TokenData, User


class TestBrandsSuccess:
    def test_get_all_brands(self, client: TestClient, users: list[User]) -> None:
        # Given
        user = users[0]
        insert_user(client, user)
        response = login_user(client, user)
        token_data: TokenData = response.json()

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

        logout_user(client, token_data["access_token"])

    def test_get_specific_brand(self, client: TestClient, users: list[User]) -> None:
        # Given
        user = users[0]
        insert_user(client, user)
        response = login_user(client, user)
        token_data: TokenData = response.json()

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

        logout_user(client, token_data["access_token"])
