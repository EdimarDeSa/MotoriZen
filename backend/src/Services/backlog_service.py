from typing import Optional
from uuid import UUID

from db.connection_handler import DBConnectionHandler, get_db_url_backlog
from Enums.backlog_event_type_enum import BacklogEventTypeEnum
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Repositories.backlog_repositry import BacklogRepository
from Services.base_service import BaseService


class BacklogService(BaseService):
    def __init__(self) -> None:
        self._backlog_repository = BacklogRepository()
        self.create_logger(__name__)

    def insert_backlog_event(
        self,
        event_type: BacklogEventTypeEnum,
        cd_user: Optional[UUID] = None,
        comment: Optional[str] = None,
    ) -> None:
        self.logger.debug("Starting insert_backlog_event")

        db_session = DBConnectionHandler.create_session(db_url=get_db_url_backlog(), write=True)

        try:
            self.logger.debug("Inserting backlog event")
            self._backlog_repository.insert_backlog_event(db_session, event_type, cd_user, comment)

            db_session.commit()

        except Exception as e:
            self.logger.exception(e)
            db_session.rollback()
            self.logger.debug("Rollbacked")
            raise e

        finally:
            db_session.close()

        self.logger.debug("Backlog event inserted")
