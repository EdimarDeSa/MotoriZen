from fastapi import FastAPI

from configs import CONTACT, REGISTER_MIDDLEWARES, REGISTER_ROUTERS, TITLE, VERSION

app = FastAPI(
    title=TITLE,
    description=TITLE,
    version=VERSION,
    contact=CONTACT,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
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
