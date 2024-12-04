import logging
import os
import sys
from logging import Handler, Logger
from pathlib import Path
from typing import Any, Callable, Sequence

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Utils.Internacionalization import InternationalizationManager

load_dotenv()

from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Middlewares import ProcessTimeHeaderMiddleware
from Routers import AuthRouter, CarsRouter, RegisterRouter, ReportsRouter, UserRouter
from Routers.base_router import BaseRouter
from Utils.custom_types import MiddlewareSequence, RoutersSequence

__all__ = [
    "REGISTER_ROUTERS",
    "REGISTER_MIDDLEWARES",
    "SWAGGER_UI_PARAMETERS",
    "CONTACT",
    "TITLE",
]


### ROUTERS ###
ROUTERS: RoutersSequence = [
    AuthRouter,
    UserRouter,
    CarsRouter,
    RegisterRouter,
    ReportsRouter,
]


def register_routers(app: FastAPI, txt_manager: InternationalizationManager) -> None:
    for router in ROUTERS:
        r = router(txt_manager=txt_manager)

        if not isinstance(r, BaseRouter):
            raise TypeError("Invalid router, must be an instance of Routers.base_router.BaseRouter")

        logger.debug(f"Starting - {r.__class__.__name__}")
        app.include_router(r.router)

        for route in r.router.routes:
            path: str = route.path if hasattr(route, "path") else str(route)
            tags: Sequence[str] = route.tags if hasattr(route, "tags") else []
            logger.debug(f"Route => {path} => {tags}")


REGISTER_ROUTERS: Callable[[FastAPI, InternationalizationManager], None] = register_routers


### MIDDLEWARES ###
ORIGINS: list[str] = ["*"]
MIDDLEWARES: MiddlewareSequence = [
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


def register_middlewares(app: FastAPI, txt_manager: InternationalizationManager) -> None:
    for middleware in MIDDLEWARES:
        logger.debug(f"Iniciando - {middleware['middleware_class'].__name__}")

        if middleware["options"].get("http"):
            app.middleware("http")(middleware["middleware_class"])
            return

        app.add_middleware(middleware["middleware_class"], **middleware["options"])


REGISTER_MIDDLEWARES: Callable[[FastAPI, InternationalizationManager], None] = register_middlewares


### PROJECT INFO ###
TITLE: str = "MotoriZen – Controle de Ganhos, KM e Consumo para Motoristas"

CONTACT: dict[str, str] = {
    "name": "Edimar de Sá",
    "email": "edimar.sa@efscode.com",
    "url": "https://efscode.com",
    "github": "https://github.com/EdimarDeSa",
    "linkedin": "https://www.linkedin.com/in/edimar-freitas-de-sá/",
}

SWAGGER_UI_PARAMETERS = {
    "docExpansion": "none",
    "deepLinking": True,
    "persistAuthorization": True,
    "displayOperationId": False,
    "displayRequestDuration": True,
    "defaultModelsExpandDepth": 0,
    "filter": True,
    "operationsSorter": "method",
    "requestSnippets": [
        {"lang": "curl", "label": "cURL"},
        {"lang": "python", "label": "Python Requests"},
    ],
    "requestTimeout": 5000,
    "showExtensions": True,
    "showCommonExtensions": True,
    "syntaxHighlight": True,
    "supportedSubmitMethods": ["get", "post", "put", "delete"],
    "tryItOutEnabled": False,
    "theme": "flattop",
}


### LOGGER ###
logger: Logger = logging.getLogger(__name__)

DEBUG_MODE: bool = bool(int(os.getenv("DEBUG_MODE", 0)))

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
