from fastapi import APIRouter, Request
from Routers.base_router import BaseRouter
from Responses import Ok
from Contents.fuel_types_content import FuelTypeContent
from DB.Models import FuelTypeModel
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Services.fuel_types_service import FuelTypesService
from Utils.custom_types import CurrentActiveUser


class FuelTypesRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/fuel-types", tags=["Fuel Types"])
        self.fuel_type_service = FuelTypesService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "/get-fuel-type/{id_fuel_type}", self.get_fuel_type, response_model=FuelTypeContent, methods=["GET"]
        )

        self.router.add_api_route(
            "/get-fuel-types", self.get_fuel_types, response_model=FuelTypeContent, methods=["POST"]
        )

    def get_fuel_types(self, request: Request, user_data: CurrentActiveUser) -> Ok:
        self.logger.debug("Starting get_fuel_types")

        try:
            fuel_types: list[FuelTypeModel] = self.fuel_type_service.get_fuel_types()

            content = FuelTypeContent(data=fuel_types)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def get_fuel_type(self, request: Request, user_data: CurrentActiveUser, id_fuel_type: int) -> Ok:
        self.logger.debug("Starting get_fuel_type")

        try:
            fuel_type: FuelTypeModel = self.fuel_type_service.get_fuel_type(id_fuel_type)

            content = FuelTypeContent(data=fuel_type)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()
