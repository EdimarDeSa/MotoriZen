from fastapi import APIRouter, Request

from Responses.created import Created
from Responses.no_content import NoContent
from Responses.ok import Ok
from Routers.base_router import BaseRouter
from Services.register_service import RegisterService


class RegisterRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/register", tags=["Register"])
        self.register_service = RegisterService()

        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/get-registers", self.get_registers, methods=["POST"], tags=["POST"])
        self.router.add_api_route("/get-register/{id_register}", self.get_register, methods=["GET"], tags=["GET"])
        self.router.add_api_route("/new-register", self.new_register, methods=["POST"], tags=["POST"])
        self.router.add_api_route("/update-register", self.update_register, methods=["PUT"], tags=["PUT"])
        self.router.add_api_route("/delete-register", self.delete_register, methods=["DELETE"], tags=["DELETE"])

    def get_registers(self, request: Request, query_data: RegistersQueryModel) -> Ok:
        raise NotImplementedError

    def get_register(self, request: Request, id_register: int) -> Ok:
        raise NotImplementedError

    def new_register(self, request: Request, new_register: NewRegisterModel) -> Created:
        raise NotImplementedError

    def update_register(self, request: Request, update_register: UpdateRegisterModel) -> NoContent:
        raise NotImplementedError

    def delete_register(self, request: Request, id_register: int) -> NoContent:
        raise NotImplementedError
