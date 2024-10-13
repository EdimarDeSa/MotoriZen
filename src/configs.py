from dotenv import load_dotenv

load_dotenv()

import logging
import os
import sys
from logging import Handler, Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

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
    rotating_handler: RotatingFileHandler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        encoding="utf-8",
        handlers=[console_handler, rotating_handler],
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    logger.info("Logger activated!")
