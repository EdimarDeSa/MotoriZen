from starlette.testclient import TestClient

from .utils.aux_functions import create_and_athenticate_user, create_vehicles
from .utils.models import Register, User, Vehicle


class TestRegistersSuccess:
    qtd_vehicles_per_user = 5
    qtd_registers_per_vehicle = 50

    def _calculate_register_offset(self, vehicle_index: int, user_index: int) -> int:
        return (
            self.qtd_registers_per_vehicle * vehicle_index
            + self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * user_index
        )

    def test_create_register(
        self, client: TestClient, users: list[User], vehicles: list[Vehicle], registers: list[Register]
    ) -> None:
        # Given
        vehicle_generator = create_vehicles(client, users, vehicles, self.qtd_vehicles_per_user)
        total_registers = self.qtd_vehicles_per_user * self.qtd_registers_per_vehicle * len(users)
        print()
        print("Total registers:", total_registers)

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


# TODO: Make tests for Registers
# TODO: Make tests for Reports
# TODO: Make tests for Errors and Exceptions
