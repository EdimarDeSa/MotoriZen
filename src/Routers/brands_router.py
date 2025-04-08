from fastapi import APIRouter, Request

from Contents.brand_content import BrandContent
from DB.Models import BrandModel
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError
from Responses import Ok
from Routers.base_router import BaseRouter
from Services.brands_service import BrandService
from Utils.custom_types import CurrentActiveUser


class BrandsRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self.router = APIRouter(prefix="/brands", tags=["Brands"])
        self.brand_service = BrandService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route("/get-brand/{id_brand}", self.get_brand, response_model=BrandContent, methods=["GET"])
        self.router.add_api_route("/get-brands", self.get_brands, response_model=BrandContent, methods=["POST"])

    def get_brand(self, request: Request, user_data: CurrentActiveUser, id_brand: int) -> Ok:
        self.logger.debug("Starting get_brands")

        try:
            brand: BrandModel = self.brand_service.get_brand(id_brand)

            content = BrandContent(data=brand)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()

    def get_brands(self, request: Request, user_data: CurrentActiveUser) -> Ok:
        self.logger.debug("Starting get_brands")

        try:
            brand: list[BrandModel] = self.brand_service.get_brands()

            content = BrandContent(data=brand)
            return Ok(content=content)

        except Exception as e:
            self.logger.exception(e)

            if not isinstance(e, MotoriZenError):
                e = MotoriZenError(err=MotoriZenErrorEnum.UNKNOWN_ERROR, detail="")

            raise e.as_http_response()
