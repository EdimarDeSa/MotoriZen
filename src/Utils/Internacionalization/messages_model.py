from pydantic import BaseModel

from Utils.Internacionalization.languages_enum import LanguageEnum


class MessageType(BaseModel):
    system_messages: dict[str, str]


class MessagesModel(BaseModel):
    messages = dict[LanguageEnum, MessageType]
