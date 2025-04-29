from starlette.testclient import TestClient

from .conftest import create_user, login_user, logout_user
from .utils.constants import PASSWORD
from .utils.models import TokenData, User


class TestUsersSuccess:
    def test_create_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            # When
            response = create_user(client, user)

            # Then
            assert response.status_code in (201, 409)  # 409 se já existir, permite execuções paralelas

    def test_logon(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            create_user(client, user)

            # When
            response = login_user(client, user)

            # Then
            assert response.status_code == 200

            # And
            token_data: TokenData = response.json()
            assert "access_token" in token_data

            logout_user(client, token_data["access_token"])

    def test_get_me(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            create_user(client, user)
            response = login_user(client, user)
            token_data: TokenData = response.json()

            # When
            response = client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 200
            assert response.json()["data"]["first_name"] == user["first_name"]

            logout_user(client, token_data["access_token"])

    def test_update_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            create_user(client, user)
            response = login_user(client, user)
            token_data: TokenData = response.json()

            # When
            response = client.put(
                "/users/update-user",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                json={"last_name": "Updated"},
            )

            # Then
            assert response.status_code == 200

            # And
            response = client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            assert response.status_code == 200
            assert response.json()["data"]["last_name"] == "Updated"

            logout_user(client, token_data["access_token"])

    def test_refresh_token(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            create_user(client, user)
            response = login_user(client, user)
            token_data: TokenData = response.json()

            # When
            response = client.post(
                "/token/refresh",
                json={"refresh_token": token_data["refresh_token"]},
            )

            # Then
            assert response.status_code == 200
            new_token = response.json()
            assert token_data["access_token"] != new_token["access_token"]

            logout_user(client, new_token["access_token"])

    def test_logout_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            create_user(client, user)
            response = login_user(client, user)
            token_data: TokenData = response.json()

            # When
            response = logout_user(client, token_data["access_token"])

            # Then
            assert response.status_code == 204

    def test_delete_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            create_user(client, user)
            response = login_user(client, user)
            token_data: TokenData = response.json()

            # When
            response = client.delete(
                "/users/delete-user",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 204
