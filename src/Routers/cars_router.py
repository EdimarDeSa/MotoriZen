from math import e

from fastapi import APIRouter, Request

from Contents.brand_content import BrandContent
from Contents.car_contents import CarContent, CarsContent
from db.Models import BrandModel, CarModel, CarNewModel, CarQueryModel, CarQueryResponseModel, CarUpdatesModel
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

        self.router.add_api_route(
            "/get-brands", self.get_brands, response_model=BrandContent, methods=["POST"], tags=["Brands"]
        )
        self.router.add_api_route(
            "/get-brand/{id_brand}",
            self.get_brand,
            response_model=BrandContent,
            methods=["POST"],
            tags=["Brands"],
        )

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
            count: int = self.car_service.get_cars_count(str(user_data.id_user), query_data.query_filters)

            car_model: list[CarModel] = self.car_service.get_cars(
                str(user_data.id_user), query_data.query_filters, query_data.query_options, count
            )

            car_query_response_model = CarQueryResponseModel(total_results=count, results=car_model)
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
            self.car_service.create_car(user_data.id_user, new_car)

            return Created()

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

    def get_brands(self, request: Request, user_data: CurrentActiveUser) -> Ok:
        self.logger.debug("Starting get_brands")

        try:
            brand: list[BrandModel] = self.car_service.get_brands()

            content = BrandContent(data=brand)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def get_brand(self, request: Request, user_data: CurrentActiveUser, id_brand: int) -> Ok:
        self.logger.debug("Starting get_brands")

        try:
            brand: BrandModel = self.car_service.get_brand(id_brand)

            content = BrandContent(data=brand)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()
