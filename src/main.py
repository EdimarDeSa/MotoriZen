from fastapi import FastAPI

from configs import CONTACT, REGISTER_MIDDLEWARES, REGISTER_ROUTERS, SWAGGER_UI_PARAMETERS, TITLE, VERSION
from Utils.Internacionalization import InternationalizationManager

app = FastAPI(
    title=TITLE,
    description=TITLE,
    version=VERSION,
    contact=CONTACT,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
)

internacionalization_manager = InternationalizationManager()

REGISTER_MIDDLEWARES(app, internacionalization_manager)
REGISTER_ROUTERS(app, internacionalization_manager)


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
