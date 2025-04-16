from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, scoped_session

from db.Querys.backlog_query_manager import BacklogQueryManager
from Enums.backlog_event_type_enum import BacklogEventTypeEnum
from Repositories.base_repository import BaseRepository


class BacklogRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._backlog_querys = BacklogQueryManager()

    def insert_backlog_event(
        self,
        db_session: scoped_session[Session],
        event_type: BacklogEventTypeEnum,
        cd_user: Optional[UUID] = None,
        comment: Optional[str] = None,
    ) -> None:
        self.logger.debug("Starting insert_backlog_event")

        try:
            query = self._backlog_querys.insert_backlog_event(event_type, cd_user, comment)

            self.logger.debug("Inserting backlog event")
            db_session.execute(query)

            self.logger.debug("Backlog event inserted")

        except Exception as e:
            raise e
