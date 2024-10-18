from fastapi import FastAPI

from configs import CONTACT, TITLE, VERSION, register_routers
from db import DBConnectionHandler


def main() -> None:
    print(TITLE)
    print(f"Contact: {CONTACT['name']} <{CONTACT['email']}>")
    print(f"Project URL: {CONTACT['url']}")

    db_session = DBConnectionHandler.create_session(write=True)
    DBConnectionHandler.test_connection(db_session)


app = FastAPI(
    title=TITLE,
    description=TITLE,
    version=VERSION,
    contact=CONTACT,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)

register_routers(app)


@app.get("/", summary="Home", tags=["Home"])
def home() -> str:
    """
    Home page
    """
    return "MotoriZen API"


@app.get("/version", summary="Version", tags=["Utils"])
def home() -> str:
    """
    Home page
    """
    return {"version": VERSION}


if __name__ == "__main__":
    main()
