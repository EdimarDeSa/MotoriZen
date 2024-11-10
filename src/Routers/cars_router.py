from fastapi import APIRouter, Request

from Contents.brand_content import BrandContent
from Contents.car_contents import CarContent, CarsContent
from DB.Models import BrandModel, CarModel, CarNewModel, CarQueryModel, CarQueryResponseModel, CarUpdatesModel
from DB.Models.car_models.car_metadata_model import CarsMetadataModel
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Responses import Created, NoContent, Ok
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
        self.router.add_api_route("/get-cars", self.get_cars, response_model=CarsContent, methods=["POST"])
        self.router.add_api_route("/get-car/{id_car}", self.get_car, response_model=CarContent, methods=["GET"])
        self.router.add_api_route("/new-car", self.new_car, methods=["POST"])
        self.router.add_api_route("/update-car", self.update_car, response_model=CarContent, methods=["PUT"])
        self.router.add_api_route("/delete-car/{id_car}", self.delete_car, response_model=None, methods=["DELETE"])

    def get_car(self, request: Request, user_data: CurrentActiveUser, id_car: str) -> Ok:
        self.logger.debug("Starting get_car")

        try:

            car_model: CarModel = self.car_service.get_car(str(user_data.id_user), id_car)

            content = CarContent(data=car_model)
            return Ok(content=content)
        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")
            raise e.as_http_response()

    def get_cars(self, request: Request, user_data: CurrentActiveUser, query_data: CarQueryModel) -> Ok:
        self.logger.debug("Starting get_cars")

        try:

            car_query_response_model = self.car_service.get_cars(
                str(user_data.id_user), query_data.query_filters, query_data.query_options
            )

            content = CarsContent(data=car_query_response_model)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")
            raise e.as_http_response()

    def new_car(self, request: Request, user_data: CurrentActiveUser, new_car: CarNewModel) -> Created:
        self.logger.debug("Starting new_car")

        try:
            self.logger.debug(f"Creating car for <user: {user_data.email}>")
            result: CarModel = self.car_service.create_car(user_data.id_user, new_car)

            content = CarContent(data=result)
            return Created(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def update_car(self, request: Request, user_data: CurrentActiveUser, update_car: CarUpdatesModel) -> Ok:
        self.logger.debug("Starting update_car")

        try:
            result: CarModel = self.car_service.update_car(
                str(user_data.id_user), str(update_car.id_car), update_car.updates
            )

            content = CarContent(data=result)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def delete_car(self, request: Request, user_data: CurrentActiveUser, id_car: str) -> NoContent:
        self.logger.debug("Starting delete_car")

        try:
            self.car_service.delete_car(str(user_data.id_user), id_car)

            return NoContent()

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()
