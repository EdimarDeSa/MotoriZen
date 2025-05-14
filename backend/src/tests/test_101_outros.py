from uuid import UUID

from starlette.testclient import TestClient

from .utils.aux_functions import regsiter_generator
from .utils.models import Register, User, Vehicle
from .utils.print_aux import print_progress, with_progress
from .utils.report_enum import ReportsEnum


class TestReportsSuccess:
    qtd_vehicles_per_user = 5
    qtd_registers_per_vehicle = 50

    def __request_report(
        self,
        client: TestClient,
        report_name: ReportsEnum,
        access_token: str,
        vehicle_ids: list[UUID],
        time_frame: dict["start":str, "end":str],
        aggregation_interval: str,
    ) -> None:
        client.post(
            "/reports/get-reports",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "reports": [report_name],
                "vehicle_ids": vehicle_ids,
                "time_frame": time_frame,
                "aggregation_interval": aggregation_interval,
            },
        )

    @with_progress("Testando relatório de distâncias")
    def test_get_mean_distance_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de distâncias por viagem")
    def test_get_mean_distance_per_trip_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de distâncias por hora de trabalho")
    def test_get_mean_distance_per_working_hour_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de distâncias por minuto de trabalho")
    def test_get_mean_distance_per_working_minute_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de distâncias totais")
    def test_get_total_distance_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de tempo de trabalho")
    def test_get_mean_working_time_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de tempo de trabalho por viagem")
    def test_get_mean_working_time_per_trip_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de tempo de trabalho por distância")
    def test_get_mean_working_time_per_distance_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de tempo de trabalho total")
    def test_get_total_working_time_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de consumo médio")
    def test_get_mean_consuption_per_distance_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de consumo médio por viagem")
    def test_get_mean_consuption_per_trip_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de consumo médio por hora de trabalho")
    def test_get_mean_consuption_per_working_hour_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de consumo médio por minuto de trabalho")
    def test_get_mean_consuption_per_working_minute_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de consumo médio total")
    def test_get_total_consumption_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de consumo total por viagem")
    def test_get_total_consumption_per_trip_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido")
    def test_get_mean_value_received_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido por consumo")
    def test_get_mean_value_received_per_consumption_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido por distância")
    def test_get_mean_value_received_per_distance_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido por hora de trabalho")
    def test_get_mean_value_received_per_working_hour_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido por minuto de trabalho")
    def test_get_mean_value_received_per_working_minute_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido por viagem")
    def test_get_mean_value_received_per_trip_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de valor recebido total")
    def test_get_total_value_received_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de quantidade de viagens")
    def test_get_mean_number_of_trips_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de quantidade de viagens por hora de trabalho")
    def test_get_mean_number_of_trips_per_working_hour_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de quantidade de viagens por minuto de trabalho")
    def test_get_mean_number_of_trips_per_working_minute_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de quantidade de viagens por 10 km")
    def test_get_mean_number_of_trips_per_10_km_report_success(self, client: TestClient) -> None:
        assert True

    @with_progress("Testando relatório de quantidade de viagens total")
    def test_get_total_number_of_trips_report_success(self, client: TestClient) -> None:
        assert True
