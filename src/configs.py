import logging
import os
import sys
from logging import Handler, Logger
from pathlib import Path
from typing import Callable, Sequence

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from starlette_sessions.middleware import SessionMiddleware
from starlette_sessions.redis.backend import RedisSessionBackend

load_dotenv()

from Enums.redis_dbs_enum import RedisDbsEnum
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


### ROUTERS ###
ROUTERS: RoutersSequence = [
    AuthRouter,
    UserRouter,
    CarsRouter,
    RegisterRouter,
    ReportsRouter,
]


def register_routers(app: FastAPI) -> None:
    for router in ROUTERS:
        r = router()

        if not isinstance(r, BaseRouter):
            raise TypeError("Invalid router, must be an instance of Routers.base_router.BaseRouter")

        logger.debug(f"Starting - {r.__class__.__name__}")
        app.include_router(r.router)

        for route in r.router.routes:
            path: str = route.path if hasattr(route, "path") else str(route)
            tags: Sequence[str] = route.tags if hasattr(route, "tags") else []
            logger.debug(f"Route => {path} => {tags}")


REGISTER_ROUTERS: Callable[[FastAPI], None] = register_routers


### MIDDLEWARES ###
PRODUCTION_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

DEVELOPMENT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

ORIGINS = PRODUCTION_ORIGINS if not DEBUG_MODE else DEVELOPMENT_ORIGINS

MIDDLEWARES: MiddlewareSequence = [
    {
        "middleware_class": CORSMiddleware,
        "options": {
            "allow_origins": ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        },
    },
    {"middleware_class": ProcessTimeHeaderMiddleware, "options": {}},
    {
        "middleware_class": SessionMiddleware,
        "options": {
            "backend": RedisSessionBackend(
                redis=Redis(
                    host=os.getenv("REDIS_HOST"),
                    port=os.getenv("REDIS_PORT"),
                    db=RedisDbsEnum.SESSIONS.value,
                ),
                ttl=600,
            ),
            "cookie_name": "session_cookie",
            "same_site": "lax",
            "https_only": False,
        },
    },
]


def register_middlewares(app: FastAPI) -> None:
    for middleware in MIDDLEWARES:
        logger.debug(f"Iniciando - {middleware['middleware_class'].__name__}")

        if middleware["options"].get("http"):
            app.middleware("http")(middleware["middleware_class"])
            return

        app.add_middleware(middleware["middleware_class"], **middleware["options"])


REGISTER_MIDDLEWARES: Callable[[FastAPI], None] = register_middlewares


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


### VERSION ###
VERSION: str = "V0.0.1"
