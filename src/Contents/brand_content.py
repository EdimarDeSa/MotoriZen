from Contents.base_content import BaseContent
from DB.Models import BrandModel


class BrandContent(BaseContent):
    data: list[BrandModel] | BrandModel
