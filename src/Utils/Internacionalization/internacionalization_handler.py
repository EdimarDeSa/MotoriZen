import json
from pathlib import Path
from typing import Any

from Utils.Internacionalization.languages_enum import LanguageEnum

from .messages_enum import MessagesEnum

# from Utils.Internacionalization.messages_model import MessagesModel


class InternationalizationManager:
    __messages_model: Any

    @classmethod
    def load_translations(cls) -> None:
        try:
            messages_file = Path(__file__).resolve().parent / "DB" / "translations.json"

            with open(messages_file, "r") as messages_buffer:
                messages_str = messages_buffer.read()
                cls.__messages_model = json.loads(messages_str)
                print("==================================")
                print(f"Messages: {cls.__messages_model}")
                print(f"Messages type: {type(cls.__messages_model)}")
                print("==================================")

        except Exception as e:
            print(f"Failed to connect to internationalization database: {e}")
            exit(-1)

    @classmethod
    def get_message(cls, language: LanguageEnum, message: MessagesEnum) -> str:
        try:
            cls.load_translations()
            lang_messages: dict[str, str] | None = cls.__messages_model.get(language, None)

            if lang_messages is None:
                raise KeyError(f"Translation not found for language '{language}' and message name '{message}'")

            _message: str = lang_messages.get(message, "Not implemented yet")
            return _message

        except Exception as e:
            print(f"Failed to retrieve translation: {e}")
            exit(-1)
