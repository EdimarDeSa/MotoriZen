from starlette.testclient import TestClient

from .utils.aux_functions import user_and_auth_generator
from .utils.models import User
from .utils.print_aux import print_progress, with_progress


class TestBrandsSuccess:
    @with_progress("Testando busca de marcas")
    def test_get_all_brands(self, client: TestClient, users: list[User]) -> None:
        # Given
        user_generator = user_and_auth_generator(client, users)
        for user_index, (token_data, _) in enumerate(user_generator):

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

            print_progress(
                f"user: {user_index + 1} / {len(users)}",
                f"{100 * (user_index + 1) / len(users)} %",
            )

    @with_progress("Testando busca de marca")
    def test_get_specific_brand(self, client: TestClient, users: list[User]) -> None:
        # Given
        user_generator = user_and_auth_generator(client, users)
        for user_index, (token_data, _) in enumerate(user_generator):

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

            print_progress(
                f"user: {user_index + 1} / {len(users)}",
                f"{100 * (user_index + 1) / len(users)} %",
            )
