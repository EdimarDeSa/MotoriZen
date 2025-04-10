import gc
import os
from datetime import datetime
from typing import cast

from fastapi import FastAPI
from redis import Redis

from configs import CONTACT, REGISTER_MIDDLEWARES, REGISTER_ROUTERS, SWAGGER_UI_PARAMETERS, TITLE, VERSION
from Contents.health_content import HealthContent
from db.connection_handler import DBConnectionHandler
from db.Models.health_model import HealthModel, HealthStatus, HealthStatusType
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from Responses.ok import Ok
from Utils.keycloak_handler import KeycloakHandler

app = FastAPI(
    title=TITLE,
    description=TITLE,
    version=VERSION,
    contact=CONTACT,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
)


REGISTER_MIDDLEWARES(app)
REGISTER_ROUTERS(app)


@app.get("/", summary="Home", tags=["Home"])
def home() -> str:
    """
    Home page
    """
    return "MotoriZen API"


@app.get("/version", summary="Version", tags=["Utils"])
def version() -> dict[str, str]:
    """
    Return the version of the API
    """
    return {"version": VERSION}


@app.get("/response-codes", summary="Response codes returned", tags=["Utils"])
def response_codes() -> dict[str, dict[str, int]]:
    """
    Returns a list of response codes and their meanings
    """
    return MotoriZenErrorEnum.as_dict()


@app.get("/health", summary="Health check", tags=["Utils"])
def health() -> Ok:
    """
    Health check
    """
    status: HealthStatusType = "Ok"
    initial_time = datetime.now()
    try:
        # Check if Redis is reachable
        redis_client = Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD"),
        )
        redis_client.ping()
        cache_status: HealthStatus = {"status": "Ok", "message": None}
        redis_client.close()  # type: ignore[no-untyped-call]
    except Exception as e:
        cache_status = {"status": "Error", "message": str(e)}
        status = "Error"

    try:
        # Check if Postgres is reachable
        db_session = DBConnectionHandler.create_session()
        DBConnectionHandler.test_connection(db_session)
        database_status: HealthStatus = {"status": "Ok", "message": None}
        db_session.close()
    except Exception as e:
        database_status = {"status": "Error", "message": str(e)}
        status = "Error"

    try:
        # Check if Keycloak is reachable
        keycloak_handler = KeycloakHandler()
        kc_status = keycloak_handler.check_health()
        auth_provider_status: HealthStatus = {"status": "Ok", "message": kc_status}
    except Exception as e:
        auth_provider_status = {"status": "Error", "message": str(e)}
        status = "Error"

    gc.collect()
    content = HealthContent(
        rc=0 if status == "Ok" else -999,
        data=HealthModel(
            status=status,
            cache_status=cache_status,
            database_status=database_status,
            auth_provider_status=auth_provider_status,
        ),
    )
    headers = {
        "X-Response-Time": str((datetime.now() - initial_time).total_seconds()),
    }
    return Ok(content=content, headers=headers)
