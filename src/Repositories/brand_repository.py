from sqlalchemy.orm import Session, scoped_session

from DB.Querys import BrandQueryManager
from DB.Schemas import BrandSchema
from Enums import MotoriZenErrorEnum
from ErrorHandler import MotoriZenError

from .base_repository import BaseRepository


class BrandRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()
        self.create_logger(__name__)
        self._car_querys = BrandQueryManager()

    def select_brands(self, db_session: scoped_session[Session]) -> list[BrandSchema]:
        self.logger.debug("Starting select_brand")

        try:
            query = self._car_querys.select_brands()

            self.logger.debug(f"Selecting all brands on table <Table: {BrandSchema.__tablename__}>")
            brand_schema: list[BrandSchema] | None = list(db_session.execute(query).scalars().all())

            if brand_schema is None:
                raise MotoriZenError(err=MotoriZenErrorEnum.BRAND_NOT_FOUND, detail="Brands not found")

            self.logger.debug(f"Brands selected")

            return brand_schema

        except Exception as e:
            raise e

    def select_brand(self, db_session: scoped_session[Session], id_brand: int) -> BrandSchema:
        self.logger.debug("Starting select_brand")

        try:
            query = self._car_querys.select_brand(id_brand)

            self.logger.debug(f"Selecting brand <id_brand: {id_brand}> on table <Table: {BrandSchema.__tablename__}>")
            brand_schema: BrandSchema | None = db_session.execute(query).scalar()

            if brand_schema is None:
                raise MotoriZenError(
                    err=MotoriZenErrorEnum.BRAND_NOT_FOUND, detail=f"Brand not faound with id: {id_brand}"
                )

            self.logger.debug(f"Brand selected <name: {brand_schema.name}>")

            return brand_schema

        except Exception as e:
            raise e
