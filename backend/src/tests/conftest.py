import json
from pathlib import Path
from typing import cast

from pytest import fixture
from starlette.testclient import TestClient

from .utils.models import Data, User, Vehicle


@fixture(scope="class")
def client() -> TestClient:
    from main import app

    return TestClient(app)


@fixture(scope="module")
def _data() -> Data:
    data_file: Path = Path(__file__).resolve().parent / "data.json"
    with open(data_file, "r") as json_file:
        raw_data = json.load(json_file)
        if raw_data is None:
            raise ValueError("Invalid data file")

    return cast(Data, raw_data)


@fixture(scope="module")
def users(_data: Data) -> list[User]:
    return _data["users"]


@fixture(scope="module")
def vehicles(_data: Data) -> list[Vehicle]:
    return _data["vehicles"]
