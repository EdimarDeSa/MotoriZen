from uuid import UUID

from fastapi import Response
from starlette.testclient import TestClient

from .utils.aux_functions import regsiter_generator
from .utils.models import Register, TokenData, User, Vehicle
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
    ) -> Response:
        return client.post(
            "/reports/get-reports",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "reports": [report_name],
                "vehicle_ids": vehicle_ids,
                "time_frame": time_frame,
                "aggregation_interval": aggregation_interval,
            },
        )

    @with_progress("Testando relatório de distâncias com intervalo de 1 dia")
    def test_get_mean_distance_report_aggregation_interval_day_success(
        self, client: TestClient, static_user_data: dict[str, str]
    ) -> None:
        # TODO: Teste deve ser em 4 testes
        # com 1 veículo time frame de 1 dia
        # com 1 veículo time frame de 5 dia
        # com 1 veículo time frame de 1 ano
        # com 5 veículos time frame de 1 dia
        # com 5 veículos time frame de 5 dia
        # com 5 veículos time frame de 1 ano
        # Given
        report_name = ReportsEnum.MEAN_DISTANCE
        vehicle_ids = static_user_data["vehicle_ids"][0]
        time_frame = {
            "start": "2024-01-01",
            "end": "2024-01-01",
        }
        aggregation_interval = "day"
        assert True

    @with_progress("Testando relatório de distâncias com intervalo de 1 semana")
    def test_get_mean_distance_report_aggregation_interval_week_success(self, client: TestClient) -> None:
        # TODO: Teste deve ser em 4 testes
        # com 1 veículo time frame de 1 semana
        # com 1 veículo time frame de 1 ano
        # com 5 veículos time frame de 1 semana
        # com 5 veículos time frame de 1 ano
        assert True

    @with_progress("Testando relatório de distâncias com intervalo de 1 mês")
    def test_get_mean_distance_report_aggregation_interval_month_success(self, client: TestClient) -> None:
        # TODO: Teste deve ser em 4 testes
        # com 1 veículo time frame de 1 mês
        # com 1 veículo time frame de 1 ano
        # com 5 veículos time frame de 1 mês
        # com 5 veículos time frame de 1 ano
        assert True

    @with_progress("Testando relatório de distâncias com intervalo de 1 ano")
    def test_get_mean_distance_report_aggregation_interval_year_success(self, client: TestClient) -> None:
        # TODO: Teste deve ser em 2 testes
        # com 1 veículo time frame de 1 ano
        # com 5 veículos time frame de 1 ano
        assert True
