from fastapi import FastAPI

from configs import CONTACT, REGISTER_MIDDLEWARES, REGISTER_ROUTERS, SWAGGER_UI_PARAMETERS, TITLE, VERSION
from Enums.motorizen_error_enum import MotoriZenErrorEnum

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
    return MotoriZenErrorEnum.response_codes_as_dict()
