import os

from keycloak import KeycloakAdmin, KeycloakOpenID


class KeycloakHandler:
    def __init__(self) -> None:
        self._admin = KeycloakAdmin(
            server_url=os.getenv("KC_URL"),
            username=os.getenv("KC_USER"),
            password=os.getenv("KC_PASSWORD"),
            client_id=os.getenv("KC_CLIENT_ID"),
            client_secret_key=os.getenv("KC_CLIENT_SECRET_KEY"),
            realm_name=os.getenv("KC_REALM"),
        )

        self._open_id = KeycloakOpenID(
            server_url=os.getenv("KC_URL"),
            realm_name=os.getenv("KC_REALM"),
            client_id=os.getenv("KC_CLIENT_ID"),
            client_secret_key=os.getenv("KC_CLIENT_SECRET"),
        )

    def insert_user(self, email: str, password: str) -> str:
        user_id = self._admin.create_user(
            username=email,
            email=email,
            enabled=True,
            password=password,
        )

        return user_id

    def check_health(self) -> None:
        try:
            self._open_id.well_known()
            users = self._admin.get_users()
            print(f"Keycloak health check passed. Users: {users}")
        except Exception as e:
            raise e
