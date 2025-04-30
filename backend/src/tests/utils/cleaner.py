import json
from pathlib import Path

from main import app
from starlette.testclient import TestClient

from .aux_functions import create_and_athenticate_user, get_csrf_token
from .constants import PASSWORD
from .models import Data


def clean_database() -> None:
    print("Cleaning database...")

    data_file: Path = Path(__file__).resolve().parent.parent / "data.json"
    with open(data_file, "r") as json_file:
        raw_data: Data = json.load(json_file)
        if raw_data is None:
            raise ValueError("Invalid data file")

    users = raw_data["users"]

    client = TestClient(app)
    for user in users:
        csrf_token = get_csrf_token(client)
        response = client.post(
            "/token",
            headers={"X-CSRF-Token": csrf_token},
            data={
                "username": user["email"],
                "password": PASSWORD,
                "grant_type": "password",
            },
        )

        if response.status_code != 200:
            continue

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
