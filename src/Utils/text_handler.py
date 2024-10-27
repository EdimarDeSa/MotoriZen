import logging
from pathlib import Path

from pydantic import BaseModel

from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError


class ModelsDesciptionTexts(BaseModel):
    last_update: str
    creation: str
    page: str
    per_page: str
    sort_by: str
    sort_order: str
    total_results: str
    results: str
    id_brand: str
    brand_name: str
    id_car: str
    cd_user: str
    cd_brand: str
    renavam: str
    model: str
    year: str
    color: str
    license_plate: str
    is_active: str
    id_register: str
    cd_car: str
    odometer: str
    distance: str
    working_time: str
    mean_consuption: str
    number_of_trips: str
    total_value: str
    register_date: str
    query_filters: str
    query_options: str
    updates: str
    new_registry: str
    first_name: str
    last_name: str
    email: str
    password: str
    birthdate: str
    cd_auth: str


class TextHandler:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        self._models_description: ModelsDesciptionTexts

        self.__check_files()

        self.__read_files()

    def __check_files(self) -> None:
        self._texts_path = Path(__file__).resolve().parent.parent / "Texts"

        if not self._texts_path.exists():
            raise MotoriZenError(
                err=MotoriZenErrorEnum.CONFIG_FILE_NOT_FOUND,
                detail=f"File not found: {self._texts_path}",
            )

        self._models_description_path = self._texts_path / "models_descriptions.json"

    def __read_files(self) -> None:
        if not self._models_description_path.exists():
            raise MotoriZenError(
                err=MotoriZenErrorEnum.CONFIG_FILE_NOT_FOUND,
                detail=f"File not found: {self._models_description_path}",
            )

        with open(self._models_description_path, "r", encoding="utf-8") as file:
            self._models_description = ModelsDesciptionTexts.model_validate_json(file.read())

    @property
    def models_description(self) -> ModelsDesciptionTexts:
        if self._models_description is None:
            self.__read_files()
        return self._models_description
