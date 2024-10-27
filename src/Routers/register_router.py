import uuid

from fastapi import APIRouter, Request

from Contents.register_content import RegisterContent
from db.Models import RegisterModel, RegisterNewModel, RegistersQueryModel, RegisterUpdatesModel
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Responses import Created, NoContent, Ok
from Services.register_service import RegisterService
from Utils.custom_types import CurrentActiveUser

from .base_router import BaseRouter


class RegisterRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/register", tags=["Register"])
        self.register_service = RegisterService()

        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/get-registers", self.get_registers, methods=["POST"])
        self.router.add_api_route("/get-register/{id_register}", self.get_register, methods=["GET"])
        self.router.add_api_route("/new-register", self.new_register, methods=["POST"])
        self.router.add_api_route("/update-register", self.update_register, methods=["PUT"])
        self.router.add_api_route("/delete-register", self.delete_register, methods=["DELETE"])

    def get_registers(self, request: Request, user_data: CurrentActiveUser, query_data: RegistersQueryModel) -> Ok:
        raise NotImplementedError

    def get_register(self, request: Request, user_data: CurrentActiveUser, id_register: uuid.UUID) -> Ok:
        self.logger.debug("Starting get_register")

        try:
            register: RegisterModel = self.register_service.get_register(str(user_data.id_user), id_register)

            content = RegisterContent(data=register)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def new_register(self, request: Request, user_data: CurrentActiveUser, new_register: RegisterNewModel) -> Created:
        self.logger.debug("Starting new_register")

        try:
            self.logger.debug("Creating new register")
            self.register_service.create_register(str(user_data.id_user), new_register)

            return Created()

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def update_register(
        self, request: Request, user_data: CurrentActiveUser, update_register: RegisterUpdatesModel
    ) -> NoContent:
        self.logger.debug("Starting update_register")

        try:
            self.register_service.update_register(
                str(user_data.id_user), str(update_register.id_register), update_register.updates
            )

            return NoContent()

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def delete_register(self, request: Request, user_data: CurrentActiveUser, id_register: int) -> NoContent:
        raise NotImplementedError
