from datetime import datetime

from sqlalchemy import INTEGER, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, MappedColumn, declarative_base, mapped_column

Base: DeclarativeBase = declarative_base()


class BacklogEventSchema(Base):  # type: ignore
    __table_args__ = {"schema": "backlog"}
    __tablename__ = "tb_backlog_event"

    id_backlog_event: MappedColumn[int] = mapped_column(INTEGER(), primary_key=True, autoincrement="auto")
    cd_backlog_event_type: MappedColumn[int] = mapped_column(INTEGER(), nullable=False)
    cd_user: MappedColumn[int] = mapped_column(INTEGER(), ForeignKey("motorizen.tb_user.id_user"), nullable=False)
    comment: MappedColumn[str] = mapped_column(Text(), nullable=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
