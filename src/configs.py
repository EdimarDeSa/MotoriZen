from typing import Any, Union

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Middlewares.process_time_header_middleware import ProcessTimeHeaderMiddleware
from Routers import AuthRouter, CarsRouter, UserRouter
from Routers.base_router import BaseRouter

load_dotenv()
import logging
import os
import sys
from logging import Handler, Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from starlette.middleware.cors import CORSMiddleware

__all__ = [
    "register_routers",
    "CONTACT",
    "TITLE",
]


### ROUTERS ###
ROUTERS: list[type[BaseRouter]] = [
    AuthRouter,
    UserRouter,
    CarsRouter,
]


def register_routers(app: FastAPI) -> None:
    for router in ROUTERS:
        r = router()

        if not isinstance(r, BaseRouter):
            raise MotoriZenError(
                detail="Invalid router, must be an instance of Routers.base_router.BaseRouter",
                err=MotoriZenErrorEnum.INVALID_ROUTER,
            )

        logger.debug(f"Starting - {r.__class__.__name__}")
        app.include_router(r.router)

        for route in r.router.routes:
            logger.debug(f"Route: {list(route.methods)[0]} - {route.tags[0]} - {route.path}")


### MIDDLEWARES ###
ORIGINS: list[str] = ["*"]
MIDDLEWARES: list[dict[str, dict[str, Any] | Any]] = [
    {
        "middleware_class": CORSMiddleware,
        "options": {
            "allow_origins": ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    },
    {"middleware_class": ProcessTimeHeaderMiddleware, "options": {}},
]


def register_middlewares(app: FastAPI) -> None:
    for middleware in MIDDLEWARES:
        logger.debug(f"Iniciando - {middleware['middleware_class'].__name__}")

        if "http" in middleware.get("options"):
            app.middleware("http")(middleware["middleware_class"])
            return

        app.add_middleware(middleware["middleware_class"], **middleware["options"])


### PROJECT INFO ###
TITLE: str = "MotoriZen – Controle de Ganhos, KM e Consumo para Motoristas"

CONTACT: dict[str, str] = {
    "name": "Edimar de Sá",
    "email": "edimar.sa@efscode.com",
    "url": "https://efscode.com",
    "github": "https://github.com/EdimarDeSa",
    "linkedin": "https://www.linkedin.com/in/edimar-freitas-de-sá/",
}


### LOGGER ###
logger: Logger = logging.getLogger(__name__)

DEBUG_MODE: bool = bool(int(os.getenv("DEBUG_MODE", "0")))

if DEBUG_MODE:
    log_format: str = (
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )

    console_handler: Handler = logging.StreamHandler(stream=sys.stdout)

    log_file: Path = Path(__file__).resolve().parent / "logs" / "app.log"
    # rotating_handler: RotatingFileHandler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        encoding="utf-8",
        handlers=[console_handler],
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    logger.info("Logger activated!")


### VERSION ###
VERSION: str = "V0.0.1"
