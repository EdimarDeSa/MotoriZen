from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user, create_vehicles
from .utils.models import User, Vehicle


class TestVehiclesSuccess:
    qtd_vehicles_per_user = 5

    # def test_create_vehicle(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
    #     # Given
    #     offset_index = 0
    #     for token_data, _ in create_and_athenticate_user(client, users):
    #         for index in range(self.qtd_vehicles_per_user):
    #             offset = self.qtd_vehicles_per_user * offset_index
    #             vehicle = vehicles[index + offset]

    #             # When
    #             response = client.post(
    #                 "/vehicles/new-vehicle",
    #                 headers={"Authorization": f"Bearer {token_data['access_token']}"},
    #                 json=vehicle,
    #             )

    #             # Then
    #             assert response.status_code == 201
    #             assert response.json()["rc"] == 0
    #             assert response.json()["data"]["license_plate"] == vehicle["license_plate"]

    #         offset_index += 1

    # def test_get_all_vehicles(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
    #     # Given
    #     for _, token_data, _ in create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user):
    #         # When
    #         response = client.post(
    #             "/vehicles/get-vehicles",
    #             headers={"Authorization": f"Bearer {token_data['access_token']}"},
    #             json={
    #                 "query_filters": {},
    #                 "query_options": {"per_page": 10},
    #             },
    #         )

    #         data = response.json()
    #         results = data["data"]["results"]
    #         rc = data["rc"]

    #         # Then
    #         assert response.status_code == 200
    #         assert rc == 0
    #         assert len(results) == self.qtd_vehicles_per_user

    def test_get_specific_vehicle(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
        # Given
        for user_vehicles, token_data, _ in create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user):
            for vehicle in user_vehicles:
                id_vehicle = vehicle["id_vehicle"]

                # When
                response = client.get(
                    f"/vehicles/get-vehicle/{id_vehicle}",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                )
                body = response.json()

                # Then
                assert response.status_code == 200
                assert body["rc"] == 0
                assert body["data"] == vehicle
