from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user, create_vehicles, print_progress, with_progress
from .utils.models import User, Vehicle


class TestVehiclesSuccess:
    qtd_vehicles_per_user = 5

    def __print_progress(self, user_index, vehicle_index, offset, total_users, total_vehicles):
        print_progress(
            f"user: {user_index + 1} / {total_users}",
            f"vehicle: {vehicle_index + 1} / {self.qtd_vehicles_per_user}",
            f"{100 * (vehicle_index + offset + 1) / total_vehicles} %",
        )

    # @with_progress("Testando criação de veículos")
    # def test_create_vehicle(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
    #     # Given
    #     user_generator = create_and_athenticate_user(client, users)
    #     total_users = len(users)
    #     total_vehicles = len(vehicles)

    #     for user_index, (token_data, _) in enumerate(user_generator):
    #         for vehicle_index in range(self.qtd_vehicles_per_user):
    #             offset = self.qtd_vehicles_per_user * user_index
    #             vehicle = vehicles[vehicle_index + offset]

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

    #             self.__print_progress(user_index, vehicle_index, offset, total_users, total_vehicles)

    @with_progress("Testando listagem de veículos")
    def test_get_all_vehicles(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
        # Given
        vehicle_generator = create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user)
        for user_index, (_, token_data, _) in enumerate(vehicle_generator):

            # When
            response = client.post(
                "/vehicles/get-vehicles",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                json={
                    "query_filters": {},
                    "query_options": {"per_page": 10},
                },
            )

            data = response.json()
            rc = data["rc"]
            results = data["data"]["results"]

            # Then
            assert response.status_code == 200
            assert rc == 0
            assert len(results) == self.qtd_vehicles_per_user

            print_progress(
                f"user: {user_index + 1} / {len(users)}",
                f"{100 * (user_index + 1) / len(users)} %",
            )

    @with_progress("Testando busca de veículos")
    def test_get_specific_vehicle(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
        # Given
        vehicle_generator = create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user)
        total_users = len(users)
        total_vehicles = len(vehicles)
        for user_index, (user_vehicles, token_data, _) in enumerate(vehicle_generator):
            for vehicle_index, vehicle in enumerate(user_vehicles):
                offset = self.qtd_vehicles_per_user * user_index
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

                self.__print_progress(user_index, vehicle_index, offset, total_users, total_vehicles)

    @with_progress("Testando atualização de veículos")
    def test_update_vehicle(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
        # Given
        vehicle_generator = create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user)
        total_users = len(users)
        total_vehicles = len(vehicles)
        for user_index, (user_vehicles, token_data, _) in enumerate(vehicle_generator):
            for vehicle_index, vehicle in enumerate(user_vehicles):
                offset = self.qtd_vehicles_per_user * user_index
                id_vehicle = vehicle["id_vehicle"]
                new_model = ""

                # When
                response = client.put(
                    f"/vehicles/update-vehicle",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                    json={"id_vehicle": id_vehicle, "updates": {"model": new_model}},
                )
                body = response.json()
                updated_model = body["data"]["model"]

                # Then
                assert response.status_code == 200
                assert body["rc"] == 0
                assert updated_model == new_model

                self.__print_progress(user_index, vehicle_index, offset, total_users, total_vehicles)

    @with_progress("Testando exclusão de veículos")
    def test_delete_vehicle(self, client: TestClient, users: list[User], vehicles: list[Vehicle]) -> None:
        # Given
        vehicle_generator = create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user)
        total_users = len(users)
        total_vehicles = len(vehicles)
        for user_index, (user_vehicles, token_data, _) in enumerate(vehicle_generator):
            for vehicle_index, vehicle in enumerate(user_vehicles):
                offset = self.qtd_vehicles_per_user * user_index
                id_vehicle = vehicle["id_vehicle"]

                # When
                response = client.delete(
                    f"/vehicles/delete-vehicle/{id_vehicle}",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                )

                # Then
                assert response.status_code == 204

                self.__print_progress(user_index, vehicle_index, offset, total_users, total_vehicles)
