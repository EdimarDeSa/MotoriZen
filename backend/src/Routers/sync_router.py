from fastapi import APIRouter, Request

from Contents.sync_content import SyncContent, SyncInitialContent
from db.Models.sync_models.sync_initial_model import SyncInitialModel
from Enums.motorizen_error_enum import MotoriZenErrorEnum
from ErrorHandler.motorizen_error import MotoriZenError
from Responses.no_content import NoContent
from Responses.ok import Ok
from Routers.base_router import BaseRouter
from Services.sync_service import SyncService
from Utils.custom_types import CurrentActiveUser


# TODO: Criar rotas de sincronização para app mobile
class SyncRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/sync", tags=["Sync"])
        self.sync_service = SyncService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/initial", self.sync_initial, response_model=SyncInitialContent, methods=["GET"])
        self.router.add_api_route(
            "/{last_pulled_at:str}", self.sync_last_pulled_at, response_model=SyncContent, methods=["GET"]
        )
        self.router.add_api_route("", self.sync_updates, methods=["POST"])

    def sync_initial(self, request: Request, user_data: CurrentActiveUser) -> Ok:
        try:
            data: SyncInitialModel = self.sync_service.sync_initial(user_data.id_user)

            content = SyncInitialContent.model_validate(data)
            return Ok(content=content)
        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def sync_last_pulled_at(self, request: Request, user_data: CurrentActiveUser, last_pulled_at: str) -> Ok:
        try:
            content = self.sync_service.sync_last_pulled_at(user_data.id_user, last_pulled_at)
            return Ok()
        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def sync_updates(self, request: Request, user_data: CurrentActiveUser) -> NoContent:
        try:
            self.sync_service.sync_updates(user_data.id_user)
            return NoContent()
        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    pass
