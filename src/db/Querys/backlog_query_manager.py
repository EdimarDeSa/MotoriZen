from typing import Optional
from uuid import UUID

from sqlalchemy import Insert, ScalarSelect, Select, insert, select

from db.Querys.base_query_manager import BaseQueryManager
from db.Schemas.backlog_event_schema import BacklogEventSchema
from db.Schemas.user_schema import UserSchema
from Enums.backlog_event_type_enum import BacklogEventTypeEnum


class BacklogQueryManager(BaseQueryManager):
    def insert_backlog_event(
        self,
        event_type: BacklogEventTypeEnum,
        cd_user: Optional[UUID] = None,
        comment: Optional[str] = None,
    ) -> Insert:
        """
        Functio to insert new backlog event

        Args:
            event_type (BacklogEventTypeEnum): Type of the event.
            cd_user (Optional[UUID], optional): Id of the user that trigger the event. Defaults to System.
            comment (Optional[str], optional): Description or comments about event trigger. Defaults to Null.

        Returns:
            Insert: _description_
        """
        if cd_user is None:
            cd_user = self.select_system_account()  # type:ignore

        return insert(BacklogEventSchema).values(
            cd_backlog_event_type=event_type,
            cd_user=cd_user,
            comment=comment,
        )

    def select_system_account(self) -> ScalarSelect[UUID]:
        return select(UserSchema.id_user).where(UserSchema.email == "motorizen@efscode.com.br").scalar_subquery()
