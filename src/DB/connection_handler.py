import logging
import os
import time
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

logger = logging.getLogger(__name__)


def get_db_url() -> str:
    db_dialect: str = os.getenv("DB_DIALECT", "postgresql")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")
    db_ip: str = os.getenv("DB_IP", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "postgres")

    return f"{db_dialect}://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}"


class DBConnectionHandler:
    @staticmethod
    def create_session(*, db_url: Optional[str] = None, write: bool = False) -> scoped_session[Session]:
        if db_url is None:
            db_url = get_db_url()

        engine: Engine = create_engine(
            db_url, pool_size=250, max_overflow=50, pool_use_lifo=True, pool_pre_ping=True, pool_recycle=300
        )

        if write:
            return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    @staticmethod
    def test_connection(db_session: scoped_session[Session]) -> None:
        retries, max_retries = 0, 5
        logger.debug("Testing database connection...")
        while retries < max_retries:
            try:
                result: str = db_session.execute(text("SELECT 1"))  # type: ignore
                logger.debug(f"Connection successful: {result}")
                break
            except Exception as e:
                retries += 1
                logger.error(f"Retrying ({retries}/{max_retries}) due to error: {e}")
                time.sleep(5)
                if retries == max_retries:
                    logger.error("Max retries reached. Exiting...")
                    exit(-1)
