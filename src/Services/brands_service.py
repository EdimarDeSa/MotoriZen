from DB.Models import BrandModel
from DB.Schemas import BrandSchema
from Enums import RedisDbsEnum
from Repositories.brand_repository import BrandRepository

from .base_service import BaseService


class BrandService(BaseService):
    def __init__(self) -> None:
        self._brand_repository = BrandRepository()
        self.create_logger(__name__)

    def get_brands(self) -> list[BrandModel]:
        self.logger.debug("Starting get_brands")
        db_session = self.create_session(write=False)

        try:
            hash_data = {"get_brands": "all_brands"}
            hash_key = self.create_hash_key(hash_data)

            brand_schema_list = self.cache_handler.get_data(RedisDbsEnum.BRANDS, hash_key)

            if brand_schema_list is None:
                self.logger.debug("Geting all brands")
                brand_schema_list = self._brand_repository.select_brands(db_session)

                brand_list = [schema.as_dict(exclude_none=True) for schema in brand_schema_list]

                self.cache_handler.set_data(RedisDbsEnum.BRANDS, hash_key, brand_list)

            return [BrandModel.model_validate(brand_schema, from_attributes=True) for brand_schema in brand_schema_list]

        except Exception as e:
            raise e

        finally:
            db_session.close()

    def get_brand(self, id_brand: int) -> BrandModel:
        self.logger.debug("Starting get_brands")
        db_session = self.create_session(write=False)

        try:
            self.logger.debug("Geting all brands")
            brand_schema: BrandSchema = self._brand_repository.select_brand(db_session, id_brand)

            return BrandModel.model_validate(brand_schema, from_attributes=True)

        except Exception as e:
            raise e

        finally:
            db_session.close()
