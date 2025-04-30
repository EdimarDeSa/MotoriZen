from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user, get_csrf_token, insert_user, login_user
from .utils.constants import PASSWORD
from .utils.models import TokenData, User


class TestUsersSuccess:
    def test_create_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            csrf_token = get_csrf_token(client)

            # When
            response = client.post(
                "/users/new-user",
                headers={"X-CSRF-Token": csrf_token},
                json={"password": PASSWORD, **user},
            )

            # Then
            assert response.status_code in (201, 409)  # 409 se já existir, permite execuções paralelas

    def test_logon(self, client: TestClient, users: list[User]) -> None:
        # Given
        for user in users:
            insert_user(client, user)
            csrf_token = get_csrf_token(client)

            # When
            response = client.post(
                "/token",
                headers={"X-CSRF-Token": csrf_token},
                data={
                    "username": user["email"],
                    "password": PASSWORD,
                    "grant_type": "password",
                },
            )

            # Then
            assert response.status_code == 200

            # And when
            token_data: TokenData = response.json()

            # Then
            assert "access_token" in token_data

    def test_get_me(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, user in create_and_athenticate_user(client, users):

            # When
            response = client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 200
            assert response.json()["data"]["first_name"] == user["first_name"]

    def test_update_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

            # When
            response = client.put(
                "/users/update-user",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                json={"last_name": "Updated"},
            )

            # Then
            assert response.status_code == 200
            assert response.json()["data"]["last_name"] == "Updated"

            # And when
            response = client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 200
            assert response.json()["data"]["last_name"] == "Updated"

    def test_refresh_token(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

            # When
            response = client.post(
                "/token/refresh",
                json={"refresh_token": token_data["refresh_token"]},
            )
            new_token = response.json()

            # Then
            assert response.status_code == 200
            assert token_data["access_token"] != new_token["access_token"]

    def test_logout_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

            # When
            response = client.get(
                "/token/logout",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 204

    def test_delete_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        for token_data, _ in create_and_athenticate_user(client, users):

            # When
            response = client.delete(
                "/users/delete-user",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 204
