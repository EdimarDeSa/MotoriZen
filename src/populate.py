import json
import logging
import random
import sys
from datetime import date, datetime, time
from pathlib import Path
from typing import TypedDict

from faker import Faker
from fastapi.testclient import TestClient

from DB.Models.register_models.register_new_model import RegisterNewModel
from main import app

log_format: str = (
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)

console_handler: logging.Handler = logging.StreamHandler(stream=sys.stdout)

log_file: Path = Path(__file__).resolve().parent / "logs" / "app.log"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    encoding="utf-8",
    handlers=[console_handler],
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class User(TypedDict):
    first_name: str
    last_name: str
    email: str
    birthdate: str
    password: str


class Car(TypedDict):
    cd_brand: int
    renavam: str
    model: str
    year: int
    color: str
    license_plate: str
    odometer: float


class Register(TypedDict):
    distance: float
    working_time: str
    mean_consuption: float
    number_of_trips: int
    total_value: float
    register_date: str


class Data(TypedDict):
    users: list[User]
    cars: list[Car]
    registers: list[Register]


if __name__ == "__main__":
    logger.debug("Starting database population...")
    logger.debug("Creating client...")

    client = TestClient(app)

    data_path = Path(__file__).resolve().parent.parent / "fake_data.json"
    logger.debug("Reading data...")
    with open(data_path, "r") as json_data:
        data: Data = json.load(json_data)
    logger.debug("Data found")

    # faker = Faker("pt_br")

    # registros = []

    # for x in range(4_000):
    #     register: Register = Register(
    #         distance=random.randint(1, 500),
    #         working_time=time(
    #             hour=(random.randint(0, 13)),
    #             minute=random.randint(0, 59),
    #             second=random.randint(0, 59),
    #         ).strftime(r"%H:%M:%S"),
    #         mean_consuption=round(random.random() * random.randint(1, 800), 2),
    #         number_of_trips=random.randint(1, 50),
    #         total_value=round(random.random() * random.randint(1, 3000), 2),
    #         register_date=faker.date_this_year().strftime(r"%Y-%m-%d"),
    #     )

    #     logger.debug(f"register created: {register}")
    #     registros.append(register)

    # data["registers"] = registros

    # new_data_path = Path(__file__).resolve().parent.parent / "new_fake_data.json"
    # with open(new_data_path, "w") as json_file:
    #     json.dump(data, json_file, indent=4)

    # exit()

    logger.debug(f"Data recovered")

    total_data = len(data["users"])
    for index in range(0, total_data, 1):
        user = data["users"][index]
        response = client.post("/users/new-user", json=user)
        logger.debug(f"User created with status code")
        # time.sleep(1)

        response = client.post("/token", data={"username": user["email"], "password": user["password"]})
        token_data = response.json()
        access_token = token_data["access_token"]
        logger.debug(f"Token received")
        # time.sleep(1)

        logged_header = {"Authorization": f"Bearer {access_token}"}

        response = client.get("/users/me", headers=logged_header)

        user_data = response.json()["data"]
        logger.debug(f"User data")
        # time.sleep(1)

        car = data["cars"][index]
        new_car = {**car}
        new_car["cd_user"] = user_data["id_user"]

        logger.debug("=========================================")
        logger.debug(f"Registering car")
        # time.sleep(1)

        response = client.post("/cars/new-car", json=new_car, headers=logged_header)
        logger.debug(f"Car created with status code")
        # time.sleep(1)

        response = client.post("/cars/get-cars", headers=logged_header, json={"query_data": {}})
        car_data = response.json()["data"]["results"][0]

        logger.debug("=========================================")
        logger.debug(f"Creating registers for car and user")

        offset = index * 10
        for reg_num in range(400):
            register = data["registers"][offset + reg_num]
            new_register = {**register}
            new_register["cd_user"] = user_data["id_user"]
            new_register["cd_car"] = car_data["id_car"]
            logger.debug(f"Reg: {new_register}")

            reg = RegisterNewModel.model_validate(new_register)
            logger.debug(f"Reg: {reg}")

            logger.debug("=========================================")
            logger.debug(f"Inserting register for car: {new_register['cd_car']}")

            response = client.post("/register/new-register", headers=logged_header, json=new_register)
            logger.debug(f"New register inserted with status code: {response.status_code}")

        response = client.get("/logout", headers=logged_header)
        logger.debug(f"Logged out with status code")
