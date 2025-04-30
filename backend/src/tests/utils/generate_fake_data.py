import json
from pathlib import Path

from faker import Faker

faker = Faker("pt_BR")

# get json data path
base_file = Path(__file__).resolve().parent.parent / "data.json"
qtd_users = 10
qtd_vehicles_per_user = 5
qtd_registers_per_vehicle = 50

# Calculate qtd total
qtd_vehicles = qtd_users * qtd_vehicles_per_user
qtd_registers = qtd_vehicles * qtd_registers_per_vehicle

# Generate usesrs
users = [
    {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "birthdate": faker.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"),
    }
    for _ in range(qtd_users)
]


# Generate vehicle list
vehicles = [
    {
        "cd_brand": faker.random_int(min=1, max=108),
        "renavam": str(faker.random_number(digits=11, fix_len=True)),
        "model": faker.word(),
        "year": faker.year(),
        "color": faker.color_name(),
        "license_plate": faker.license_plate(),
        "cd_fuel_type": faker.random_int(min=1, max=4),
        "fuel_capacity": faker.random_int(min=40, max=100),
        "odometer": faker.random_int(min=0, max=100000),
        "is_active": faker.boolean(),
    }
    for _ in range(qtd_vehicles)
]

# Save data
with open(base_file, "w") as file:
    file.seek(0)
    json.dump({"users": users, "vehicles": vehicles}, file, indent=2)
