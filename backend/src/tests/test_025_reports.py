from starlette.testclient import TestClient

from .utils.aux_functions import (
    create_registers,
    create_vehicles,
    print_progress,
    with_progress,
)
from .utils.models import Register, User, Vehicle


class TestReportsSuccess:
    qtd_vehicles_per_user = 5
    qtd_registers_per_vehicle = 50

    def _calculate_register_offset(self, vehicle_index: int, user_index: int) -> int:
        return (
            self.qtd_registers_per_vehicle * vehicle_index
            + self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * user_index
        )

    @with_progress("Testando criação de registros")
    def test_create_register(
        self, client: TestClient, users: list[User], vehicles: list[Vehicle], registers: list[Register]
    ) -> None:
        # Given

        vehicle_generator = create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user)
        total_registers = self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * len(users)

        for user_index, (user_vehicles, token_data, _) in enumerate(vehicle_generator):
            for vehicle_index, vehicle in enumerate(user_vehicles):
                vehicle_odometer = vehicle["odometer"]

                for register_index in range(self.qtd_registers_per_vehicle):
                    offset = self._calculate_register_offset(vehicle_index, user_index)

                    register = registers[register_index + offset]
                    vehicle_odometer += register["distance"]

                    register["cd_vehicle"] = vehicle["id_vehicle"]

                    # When
                    response = client.post(
                        "/register/new-register",
                        headers={"Authorization": f"Bearer {token_data['access_token']}"},
                        json=register,
                    )

                    register_data = response.json()["data"]["register_data"]
                    vehicle_data = response.json()["data"]["vehicle_data"]

                    # Then
                    assert response.status_code == 201
                    assert response.json()["rc"] == 0
                    assert register_data["cd_vehicle"] == vehicle_data["id_vehicle"] == vehicle["id_vehicle"]
                    assert register_data["distance"] == register["distance"]
                    assert vehicle_data["odometer"] == vehicle_odometer

                    print(
                        "Processed:".ljust(12),
                        f"user: {user_index + 1:>3} / {len(users):<3}",
                        f"vehicle: {vehicle_index + 1:>3} / {self.qtd_vehicles_per_user:<3}",
                        f"register: {register_index + offset + 1:>4} / {total_registers:<4}",
                        f"{100 * (register_index + offset + 1) / total_registers:>6.2f}%",
                        sep="\t|\t",
                        end="\r",
                    )

    @with_progress("Testando busca de registros")
    def test_get_all_registers(
        self, client: TestClient, users: list[User], vehicles: list[Vehicle], registers: list[Register]
    ) -> None:
        # Given
        register_generator = create_registers(
            client, users, vehicles, registers, self.qtd_vehicles_per_user, self.qtd_registers_per_vehicle
        )
        total_users = len(users)
        total_registers = self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * len(users)

        for user_index, (_, token_data, _, stored_registers) in enumerate(register_generator):
            # When
            response = client.post(
                "/register/get-registers",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                json={
                    "query_filters": {},
                    "query_options": {"per_page": 500},
                },  # 500 pois atualmente o teste cria 250 registros
            )

            # Then
            assert response.status_code == 200
            assert response.json()["rc"] == 0
            assert len(response.json()["data"]["results"]) == len(stored_registers)

            print_progress(
                f"user: {user_index + 1} / {total_users}",
                f"Registros: {250 * (user_index + 1):>3} / {total_registers:<3}",
                f"{100 * (user_index + 1) / total_users:>6.2f}%",
            )

    @with_progress("Testando busca de um registro")
    def test_get_specific_register(
        self, client: TestClient, users: list[User], vehicles: list[Vehicle], registers: list[Register]
    ) -> None:
        # Given
        register_generator = create_registers(
            client, users, vehicles, registers, self.qtd_vehicles_per_user, self.qtd_registers_per_vehicle
        )
        total_users = len(users)
        total_registers = self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * len(users)

        for user_index, (_, token_data, _, stored_registers) in enumerate(register_generator):
            # When
            for register_index, stored_register in enumerate(stored_registers):
                register_offset = (
                    register_index + user_index * self.qtd_registers_per_vehicle * self.qtd_vehicles_per_user
                )
                id_register = stored_register.id_register
                response = client.get(
                    f"/register/get-register/{id_register}",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                )

                # Then
                assert response.status_code == 200
                assert response.json()["rc"] == 0
                assert response.json()["data"]["id_register"] == str(stored_register.id_register)

                print_progress(
                    f"user: {user_index + 1} / {total_users}",
                    f"Register: {register_offset + 1:>3} / {total_registers:<3}",
                    f"{100 * (register_offset + 1) / total_registers:>6.2f}%",
                )

    @with_progress("Testando atualização de um registro")
    def test_update_register(
        self, client: TestClient, users: list[User], vehicles: list[Vehicle], registers: list[Register]
    ) -> None:
        # Given
        register_generator = create_registers(
            client, users, vehicles, registers, self.qtd_vehicles_per_user, self.qtd_registers_per_vehicle
        )
        total_users = len(users)
        total_registers = self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * len(users)

        for user_index, (_, token_data, _, stored_registers) in enumerate(register_generator):
            # When
            for register_index, stored_register in enumerate(stored_registers):
                register_offset = (
                    register_index + user_index * self.qtd_registers_per_vehicle * self.qtd_vehicles_per_user
                )
                id_register = str(stored_register.id_register)
                new_total_value = 500.20
                response = client.put(
                    "/register/update-register",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                    json={
                        "id_register": id_register,
                        "updates": {
                            "total_value": new_total_value,
                        },
                    },
                )

                # Then
                assert response.status_code == 204

                response = client.get(
                    f"/register/get-register/{id_register}",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                )

                # Then
                assert response.json()["rc"] == 0
                assert response.json()["data"]["id_register"] == id_register
                assert response.json()["data"]["total_value"] == new_total_value
                assert response.json()["data"]["total_value"] != stored_register.total_value

                print_progress(
                    f"user: {user_index + 1} / {total_users}",
                    f"Register: {register_offset + 1:>3} / {total_registers:<3}",
                    f"{100 * (register_offset + 1) / total_registers:>6.2f}%",
                )

    @with_progress("Testando exclusão de um registro")
    def test_delete_register(
        self, client: TestClient, users: list[User], vehicles: list[Vehicle], registers: list[Register]
    ) -> None:
        # Given
        register_generator = create_registers(
            client, users, vehicles, registers, self.qtd_vehicles_per_user, self.qtd_registers_per_vehicle
        )
        total_users = len(users)
        total_registers = self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * len(users)

        for user_index, (_, token_data, _, stored_registers) in enumerate(register_generator):
            # When
            for register_index, stored_register in enumerate(stored_registers):
                register_offset = (
                    register_index + user_index * self.qtd_registers_per_vehicle * self.qtd_vehicles_per_user
                )
                id_register = stored_register.id_register
                response = client.delete(
                    f"/register/delete-register/{id_register}",
                    headers={"Authorization": f"Bearer {token_data['access_token']}"},
                )

                # Then
                assert response.status_code == 204

                print_progress(
                    f"user: {user_index + 1} / {total_users}",
                    f"Register: {register_offset + 1:>3} / {total_registers:<3}",
                    f"{100 * (register_offset + 1) / total_registers:>6.2f}%",
                )
