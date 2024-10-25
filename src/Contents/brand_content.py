from Contents.base_content import BaseContent
from db.Models import BrandModel


class BrandContent(BaseContent):
    data: list[BrandModel] | BrandModel
