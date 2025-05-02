from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user, get_csrf_token, insert_user, print_progress, with_progress
from .utils.constants import PASSWORD
from .utils.models import TokenData, User


class TestUsersSuccess:
    def __print_progress(self, user_index, total_users) -> None:
        print_progress(
            f"user: {user_index} / {total_users}",
            f"{100 * user_index / total_users} %",
        )

    @with_progress("Testando criação de usuários")
    def test_create_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        for user_index, user in enumerate(users):
            csrf_token = get_csrf_token(client)

            # When
            response = client.post(
                "/users/new-user",
                headers={"X-CSRF-Token": csrf_token},
                json={"password": PASSWORD, **user},
            )

            # Then
            assert response.status_code in (201, 409)  # 409 se já existir, permite execuções paralelas

            self.__print_progress(user_index + 1, total_users)

    @with_progress("Testando logon")
    def test_logon(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        for user_index, user in enumerate(users):
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

            self.__print_progress(user_index + 1, total_users)

    @with_progress("Testando busca de usuários")
    def test_get_me(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        user_generator = create_and_athenticate_user(client, users)
        for user_index, (token_data, user) in enumerate(user_generator):

            # When
            response = client.get(
                "/users/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 200
            assert response.json()["data"]["first_name"] == user["first_name"]

            self.__print_progress(user_index + 1, total_users)

    @with_progress("Testando alteração de usuários")
    def test_update_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        user_generator = create_and_athenticate_user(client, users)
        for user_index, (token_data, _) in enumerate(user_generator):

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

            self.__print_progress(user_index + 1, total_users)

    @with_progress("Testando refresh token")
    def test_refresh_token(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        user_generator = create_and_athenticate_user(client, users)
        for user_index, (token_data, _) in enumerate(user_generator):

            # When
            response = client.post(
                "/token/refresh",
                json={"refresh_token": token_data["refresh_token"]},
            )
            new_token = response.json()

            # Then
            assert response.status_code == 200
            assert token_data["access_token"] != new_token["access_token"]

            self.__print_progress(user_index + 1, total_users)

    @with_progress("Testando logout")
    def test_logout_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        user_generator = create_and_athenticate_user(client, users)
        for user_index, (token_data, _) in enumerate(user_generator):

            # When
            response = client.get(
                "/token/logout",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 204

            self.__print_progress(user_index + 1, total_users)

    @with_progress("Testando exclusão de usuários")
    def test_delete_user(self, client: TestClient, users: list[User]) -> None:
        # Given
        total_users = len(users)
        user_generator = create_and_athenticate_user(client, users)
        for user_index, (token_data, _) in enumerate(user_generator):

            # When
            response = client.delete(
                "/users/delete-user",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            # Then
            assert response.status_code == 204

            self.__print_progress(user_index + 1, total_users)
