from main import app
from starlette.testclient import TestClient

from .aux_functions import get_csrf_token
from .constants import PASSWORD
from .data_base_aux import DBConnectionHandler, UserSchema


def clean_database() -> None:
    print("Cleaning database...")

    db_session = DBConnectionHandler.create_session(write=True)

    user_emails = [
        email[0]
        for email in db_session.query(UserSchema.email).filter(UserSchema.email != "motorizen@efscode.com.br").all()
    ]

    db_session.close()

    if not user_emails:
        print("Database already clean.")
        return

    client = TestClient(app)
    for email in user_emails:
        csrf_token = get_csrf_token(client)
        response = client.post(
            "/token",
            headers={"X-CSRF-Token": csrf_token},
            data={
                "username": email,
                "password": PASSWORD,
                "grant_type": "password",
            },
        )

        token_data = response.json()

        client.delete(
            "/users/delete-user",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )

    print("Database cleaned.")


if __name__ == "__main__":
    import sys

    clean_database()

    sys.exit(0)
