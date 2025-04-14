from fastapi import APIRouter, Request

from Contents.vehicle_content import VehiclesContent
from Contents.vehicle_contents import VehicleContent
from db.Models import VehicleModel, VehicleNewModel, VehicleQueryModel, VehicleUpdatesModel
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Responses import Created, NoContent, Ok
from Routers.base_router import BaseRouter
from Services.vehicle_service import VehicleService
from Utils.custom_types import CurrentActiveUser


class VehiclesRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/vehicles", tags=["Vehicles"])
        self.vehicle_service = VehicleService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/get-vehicles", self.get_vehicles, response_model=VehiclesContent, methods=["POST"])
        self.router.add_api_route(
            "/get-vehicle/{id_vehicle}", self.get_vehicle, response_model=VehicleContent, methods=["GET"]
        )
        self.router.add_api_route("/new-vehicle", self.new_vehicle, methods=["POST"])
        self.router.add_api_route(
            "/update-vehicle", self.update_vehicle, response_model=VehicleContent, methods=["PUT"]
        )
        self.router.add_api_route(
            "/delete-vehicle/{id_vehicle}", self.delete_vehicle, response_model=None, methods=["DELETE"]
        )

    def get_vehicle(self, request: Request, user_data: CurrentActiveUser, id_vehicle: str) -> Ok:
        self.logger.debug("Starting get_vehicle")

        try:

            VEHICLE_MODEL: VehicleModel = self.vehicle_service.get_vehicle(str(user_data.id_user), id_vehicle)

            content = VehicleContent(data=VEHICLE_MODEL)
            return Ok(content=content)
        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")
            raise e.as_http_response()

    def get_vehicles(self, request: Request, user_data: CurrentActiveUser, query_data: VehicleQueryModel) -> Ok:
        self.logger.debug("Starting get_vehicles")

        try:

            vehicles_query_response_model = self.vehicle_service.get_vehicles(
                str(user_data.id_user), query_data.query_filters, query_data.query_options
            )

            content = VehiclesContent(data=vehicles_query_response_model)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")
            raise e.as_http_response()

    def new_vehicle(self, request: Request, user_data: CurrentActiveUser, new_vehicle: VehicleNewModel) -> Created:
        self.logger.debug("Starting new_vehicle")

        try:
            self.logger.debug(f"Creating vehicle for <user: {user_data.email}>")
            result: VehicleModel = self.vehicle_service.create_vehicle(user_data.id_user, new_vehicle)

            content = VehicleContent(data=result)
            return Created(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def update_vehicle(self, request: Request, user_data: CurrentActiveUser, update_vehicle: VehicleUpdatesModel) -> Ok:
        self.logger.debug("Starting update_vehicle")

        try:
            result: VehicleModel = self.vehicle_service.update_vehicle(
                str(user_data.id_user), str(update_vehicle.id_vehicle), update_vehicle.updates
            )

            content = VehicleContent(data=result)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def delete_vehicle(self, request: Request, user_data: CurrentActiveUser, id_vehicle: str) -> NoContent:
        self.logger.debug("Starting delete_vehicle")

        try:
            self.vehicle_service.delete_vehicle(str(user_data.id_user), id_vehicle)

            return NoContent()

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()
