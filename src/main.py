from fastapi import FastAPI

from configs import CONTACT, TITLE, VERSION, register_middlewares, register_routers

app = FastAPI(
    title=TITLE,
    description=TITLE,
    version=VERSION,
    contact=CONTACT,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)

register_middlewares(app)
register_routers(app)


@app.get("/", summary="Home", tags=["Home"])
def home() -> str:
    """
    Home page
    """
    return "MotoriZen API"


@app.get("/version", summary="Version", tags=["Utils"])
def home() -> dict[str, str]:
    """
    Return the version of the API
    """
    return {"version": VERSION}
