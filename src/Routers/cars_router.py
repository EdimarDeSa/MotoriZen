from math import e

from fastapi import APIRouter, Request

from Contents.car_contents import CarContent
from db.Models import NewCarModel, UpdateCarModel
from db.Models.car_model import CarModel
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Responses.created import Created
from Responses.ok import Ok
from Routers.base_router import BaseRouter
from Services.car_service import CarService
from Utils.custom_types import CurrentActiveUser


class CarsRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/cars", tags=["Cars"])
        self.car_service = CarService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/get-car/{car_id}", self.get_car, response_model=CarContent, methods=["GET"])
        self.router.add_api_route("/get-cars", self.get_cars, methods=["GET"])
        self.router.add_api_route("/new-car", self.new_car, methods=["POST"])
        self.router.add_api_route("/update-car/{car_id}", self.update_car, methods=["PUT"])
        self.router.add_api_route("/delete-car/{car_id}", self.delete_car, methods=["DELETE"])

    def get_car(self, request: Request, user_data: CurrentActiveUser, car_id: str) -> Ok:
        self.logger.debug("Starting get_car")

        try:

            car_schema: CarModel = self.car_service.get_car(str(user_data.id_user), car_id)

            content = CarContent(data=car_schema)
            return Ok(content=content)
        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")
            raise e.as_http_response()

    def get_cars(self, request: Request, user_data: CurrentActiveUser) -> None:
        raise NotImplementedError("Method not implemented yet.")

    def new_car(self, request: Request, user_data: CurrentActiveUser, new_car: NewCarModel) -> Created:
        self.logger.debug("Starting new_car")

        try:
            self.logger.debug(f"Creating car for <user: {user_data.email}>")
            self.car_service.create_car(user_data.id_user, new_car)

            return Created()

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def update_car(
        self, request: Request, user_data: CurrentActiveUser, car_id: int, update_car: UpdateCarModel
    ) -> None:
        raise NotImplementedError("Method not implemented yet.")

    def delete_car(self, request: Request, user_data: CurrentActiveUser, car_id: int) -> None:
        raise NotImplementedError("Method not implemented yet.")
