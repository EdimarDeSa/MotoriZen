from Contents.base_content import BaseContent
from db.Models.brand_model import BrandModel


class BrandContent(BaseContent):
    data: list[BrandModel] | BrandModel
