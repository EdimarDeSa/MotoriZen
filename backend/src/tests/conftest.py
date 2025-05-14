import json
from pathlib import Path
from typing import cast

from pytest import fixture
from sqlalchemy import text
from starlette.testclient import TestClient

from .utils.aux_functions import (
    insert_registers,
    insert_user,
    insert_vehicles,
    login_user,
    select_user_ids,
    vehicles_already_exists,
)
from .utils.data_base_aux import DBConnectionHandler, VehicleSchema
from .utils.models import Data, Register, StaticData, StaticUserData, User, Vehicle


@fixture(scope="class")
def client() -> TestClient:
    from main import app

    return TestClient(app)


@fixture(scope="module")
def _data() -> Data:
    data_file: Path = Path(__file__).resolve().parent / "data.json"
    with open(data_file, "r") as json_file:
        raw_data: Data = json.load(json_file)
        if raw_data is None:
            raise ValueError("Invalid data file")

    return cast(Data, raw_data)


@fixture(scope="module")
def users(_data: Data) -> list[User]:
    return _data["users"]


@fixture(scope="module")
def vehicles(_data: Data) -> list[Vehicle]:
    return _data["vehicles"]


@fixture(scope="module")
def registers(_data: Data) -> list[Register]:
    return _data["registers"]


@fixture(scope="module")
def static_user_data(client: TestClient) -> StaticData:
    data_file: Path = Path(__file__).resolve().parent / "static_data.json"
    with open(data_file, "r") as json_file:
        raw_data: StaticData = json.load(json_file)
        if raw_data is None:
            raise ValueError("Invalid data file")

    for _user in raw_data["users"]:
        insert_user(client, _user)

    db_session = DBConnectionHandler.create_session(write=True)
    user_cache = select_user_ids(client, db_session, raw_data["users"])

    if (
        db_session.execute(
            text("SELECT COUNT(*) FROM tb_vehicle WHERE license_plate = :license_plate").bindparams(
                license_plate=raw_data["vehicles"][0]["license_plate"]
            )
        ).scalar()
        > 0
    ):
        insert_vehicles(
            db_session,
            raw_data["users"],
            raw_data["vehicles"],
            user_cache,
            (len(raw_data["vehicles"]) // len(raw_data["users"])),
        )
        stored_vehicles = db_session.query(VehicleSchema).all()

        insert_registers(
            db_session, stored_vehicles, (len(raw_data["registers"]) // len(raw_data["vehicles"])), registers
        )

        del user_cache
        del stored_vehicles

        db_session.commit()
    db_session.close()

    return cast(StaticData, raw_data)
