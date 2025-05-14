import calendar
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from faker import Faker

faker = Faker("pt_BR")

# Configurações
base_file = Path(__file__).resolve().parent.parent / "static_data.json"
qtd_users = 10
qtd_vehicles_per_user = 5
qtd_registers_per_vehicle = 50

# Dados de referência para uso repetido
FUEL_TYPES = [1, 2, 3, 4]
BRANDS = list(range(1, 109))
YEARS = list(range(2010, 2025))


def default_report_results() -> dict[str, Any]:
    return {
        "mean_distance": 0,
        "mean_distance_per_trip": 0,
        "mean_distance_per_working_hour": 0,
        "mean_distance_per_working_minute": 0,
        "total_distance": 0,
        "mean_working_time": timedelta(0),
        "mean_working_time_per_trip": timedelta(0),
        "mean_working_time_per_distance": timedelta(0),
        "total_working_time": timedelta(0),
        "mean_consumption_per_distance": 0,
        "mean_consumption_per_trip": 0,
        "mean_consumption_per_working_hour": 0,
        "mean_consumption_per_working_minute": 0,
        "total_consumption": 0,
        "total_consumption_per_trip": 0,
        "mean_value_received": 0,
        "mean_value_received_per_consumption": 0,
        "mean_value_received_per_distance": 0,
        "mean_value_received_per_working_hour": 0,
        "mean_value_received_per_working_minute": 0,
        "mean_value_received_per_trip": 0,
        "total_value_received": 0,
        "mean_number_of_trips": 0,
        "mean_number_of_trips_per_working_hour": 0,
        "mean_number_of_trips_per_working_minute": 0,
        "mean_number_of_trips_per_10_km": 0,
        "total_number_of_trips": 0,
        "register_count": 0,
    }


def update_report_results(register: dict[str, Any], report_results: dict[str, Any]) -> None:
    # Converter a string de tempo em objeto timedelta
    time_parts = register["working_time"].split(":")
    working_time_delta = timedelta(hours=int(time_parts[0]), minutes=int(time_parts[1]), seconds=int(time_parts[2]))

    # Contador para calcular médias corretamente
    report_results["register_count"] += 1

    # Médias de distâncias
    report_results["mean_distance"] = report_results["total_distance"] / count

    # Atualiza os totais
    report_results["total_distance"] += register["distance"]
    report_results["total_working_time"] += datetime.strptime(register["working_time"], "%H:%M:%S")
    report_results["total_consumption"] += register["mean_consumption"] * register["distance"]
    report_results["total_value_received"] += register["total_value"]
    report_results["total_number_of_trips"] += register["number_of_trips"]

    # Recalcula todas as médias com base nos totais e contagem
    count = report_results["register_count"]

    # Atualiza os médios de distâncias
    report_results["mean_distance"] = (report_results["mean_distance"] + register["distance"]) / 2
    report_results["mean_distance_per_trip"] = (
        report_results["total_distance"] / report_results["total_number_of_trips"]
    )
    report_results["mean_distance_per_working_hour"] = report_results["total_distance"] / (
        report_results["total_working_time"].total_seconds() / 3600
    )
    report_results["mean_distance_per_working_minute"] = report_results["total_distance"] / (
        report_results["total_working_time"].total_seconds() / 60
    )

    # Atualiza os médios de tempo de trabalho
    report_results["mean_working_time"] = (
        report_results["mean_working_time"] + datetime.strptime(register["working_time"], "%H:%M:%S")
    ) / 2
    report_results["mean_working_time_per_trip"] = (
        report_results["total_working_time"] / report_results["total_number_of_trips"]
    )
    report_results["mean_working_time_per_distance"] = (
        report_results["total_working_time"] / report_results["total_distance"]
    )

    # Atualiza os médios de consumo
    report_results["mean_consumption_per_distance"] = (
        report_results["total_consumption"] / report_results["total_distance"]
    )
    report_results["mean_consumption_per_trip"] = (
        report_results["total_consumption"] / report_results["total_number_of_trips"]
    )
    report_results["mean_consumption_per_working_hour"] = report_results["total_consumption"] / (
        report_results["total_working_time"].total_seconds() / 3600
    )
    report_results["mean_consumption_per_working_minute"] = report_results["total_consumption"] / (
        report_results["total_working_time"].total_seconds() / 60
    )

    # Atualiza os médios de recebimentos
    report_results["mean_value_received"] = (report_results["mean_value_received"] + register["total_value"]) / 2
    report_results["mean_value_received_per_consumption"] = (
        report_results["total_value_received"] / report_results["total_consumption"]
    )
    report_results["mean_value_received_per_distance"] = (
        report_results["total_value_received"] / report_results["total_distance"]
    )
    report_results["mean_value_received_per_working_hour"] = report_results["total_value_received"] / (
        report_results["total_working_time"].total_seconds() / 3600
    )
    report_results["mean_value_received_per_working_minute"] = report_results["total_value_received"] / (
        report_results["total_working_time"].total_seconds() / 60
    )
    report_results["mean_value_received_per_trip"] = (
        report_results["total_value_received"] / report_results["total_number_of_trips"]
    )

    # Atualiza os médios de viagens
    report_results["mean_number_of_trips"] = (report_results["mean_number_of_trips"] + register["number_of_trips"]) / 2
    report_results["mean_number_of_trips_per_working_hour"] = report_results["total_number_of_trips"] / (
        report_results["total_working_time"].total_seconds() / 3600
    )
    report_results["mean_number_of_trips_per_working_minute"] = report_results["total_number_of_trips"] / (
        report_results["total_working_time"].total_seconds() / 60
    )
    report_results["mean_number_of_trips_per_10_km"] = report_results["total_number_of_trips"] / (
        report_results["total_distance"] / 10
    )


def generate_user_data() -> dict[str, Any]:
    """
    Gera dados de um usuário.

    Returns:
        dict[str, Any]: Dados do usuário
    """
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "birthdate": faker.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"),
    }


def generate_vehicle_data() -> dict[str, Any]:
    """
    Gera dados de um veículo.

    Returns:
        dict[str, Any]: Dados do veículo
    """
    return {
        "cd_brand": random.choice(BRANDS),
        "renavam": str(faker.random_number(digits=11, fix_len=True)),
        "model": faker.word().capitalize(),
        "year": random.choice(YEARS),
        "color": faker.color_name(),
        "license_plate": faker.license_plate(),
        "cd_fuel_type": random.choice(FUEL_TYPES),
        "fuel_capacity": round(random.uniform(40, 100), 2),
        "odometer": round(random.uniform(0, 100000), 2),
        "is_active": faker.boolean(),
    }


def generate_register(day: str) -> dict[str, Any]:
    """
    Gera um registro para uma data específica.

    Args:
        day (str): Data do registro no formato YYYY-MM-DD

    Returns:
        dict[str, Any]: Dados do registro
    """
    return {
        "number_of_trips": random.randint(1, 40),
        "distance": round(random.uniform(5, 400), 2),
        "working_time": faker.time("%H:%M:%S"),
        "mean_consumption": round(random.uniform(1, 50), 2),  # Corrigido typo
        "total_value": round(random.uniform(1, 10000), 2),
        "register_date": day,
    }


def get_last_day_of_month(year: int, month: int) -> int:
    """
    Retorna o último dia de um mês específico.

    Args:
        year (int): Ano
        month (int): Mês

    Returns:
        int: Último dia do mês
    """
    return calendar.monthrange(year, month)[1]


def generate_daily_register_data() -> list[dict[str, Any]]:
    """
    Gera registros diários.

    Returns:
        list[dict[str, Any]]: Lista de registros diários
    """
    registros_por_dia = 10
    registers = []
    for _ in range(qtd_registers_per_vehicle // registros_por_dia):
        random_date = faker.date_between(start_date=datetime(2024, 1, 1), end_date=datetime(2024, 12, 31)).strftime(
            "%Y-%m-%d"
        )
        date_registers = {random_date: []}
        report_results = default_report_results()

        for _ in range(registros_por_dia):
            register = generate_register(random_date)
            update_report_results(register, report_results)
            date_registers[random_date].append(register)

        registers.append(date_registers)

    return registers


def generate_weekly_register_data() -> list[dict[str, Any]]:
    """
    Gera registros semanais.

    Returns:
        list[dict[str, Any]]: Lista de registros semanais
    """
    registers = []
    registros_por_semana = 10

    for _ in range(qtd_registers_per_vehicle // registros_por_semana):
        random_start_week_day = faker.date_between(start_date=datetime(2024, 1, 1), end_date=datetime(2024, 12, 24))
        final_week_day = random_start_week_day + timedelta(days=6)
        week_key = f"{random_start_week_day.strftime('%Y-%m-%d')}_{final_week_day.strftime('%Y-%m-%d')}"
        week_registers = {week_key: []}

        for _ in range(registros_por_semana):
            random_day_in_week = faker.date_between(
                start_date=random_start_week_day,
                end_date=final_week_day,
            ).strftime("%Y-%m-%d")
            week_registers[week_key].append(generate_register(random_day_in_week))

        registers.append(week_registers)

    return registers


def generate_monthly_register_data() -> list[dict[str, Any]]:
    """
    Gera registros mensais.

    Returns:
        list[dict[str, Any]]: Lista de registros mensais
    """
    registers = []
    registros_por_mes = 10
    year = 2024

    for _ in range(qtd_registers_per_vehicle // registros_por_mes):
        random_month = random.randint(1, 12)
        last_day = get_last_day_of_month(year, random_month)

        start_date = datetime(year, random_month, 1)
        end_date = datetime(year, random_month, last_day)

        month_key = f"{year}-{random_month:02d}"
        month_registers = {month_key: []}

        for _ in range(registros_por_mes):
            random_day_in_month = faker.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d")
            month_registers[month_key].append(generate_register(random_day_in_month))

        registers.append(month_registers)

    return registers


def generate_yearly_register_data() -> list[dict[str, Any]]:
    """
    Gera registros anuais.

    Returns:
        list[dict[str, Any]]: Lista de registros anuais
    """
    registers = []
    registros_por_ano = 25
    years = [2023, 2024]

    for year in years:
        year_key = str(year)
        year_registers = {year_key: []}

        for _ in range(registros_por_ano):
            random_day_in_year = faker.date_between(
                start_date=datetime(year, 1, 1),
                end_date=datetime(year, 12, 31),
            ).strftime("%Y-%m-%d")
            year_registers[year_key].append(generate_register(random_day_in_year))

        registers.append(year_registers)

    return registers


def generate_structured_data() -> list[dict[str, Any]]:
    """
    Gera estrutura de dados formatada por email de usuário.

    Returns:
        dict[str, dict[str, Any]]: Dados estruturados no formato:
        [
            {
                "user_data": dict[str, Any],
                "vehicles": [
                    {
                        "vehicle_data": list[dict[str, Any]],
                        "dayly_registers": list[dict[str, Any]],
                        "weekly_registers": list[dict[str, Any]],
                        "monthly_registers": list[dict[str, Any]],
                        "yearly_registers": list[dict[str, Any]],
                    },
                    ...
                ],
            },
            ...
        ]
    """

    final_data = [
        {
            "user_data": generate_user_data(),
            "vehicles": [
                {
                    "vehicle_data": generate_vehicle_data(),
                    "dayly_registers": generate_daily_register_data(),
                    "weekly_registers": generate_weekly_register_data(),
                    "monthly_registers": generate_monthly_register_data(),
                    "yearly_registers": generate_yearly_register_data(),
                }
                for _ in range(qtd_vehicles_per_user)
            ],
        }
        for _ in range(qtd_users)
    ]

    return final_data


def main():
    strutured_data = generate_structured_data()

    # Save data
    with open(base_file, "w") as file:
        file.seek(0)
        json.dump(
            strutured_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Dados gerados com sucesso: {len(strutured_data)} usuários")
    print(f"Arquivo salvo em: {base_file}")


if __name__ == "__main__":
    main()
