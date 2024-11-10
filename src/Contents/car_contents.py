from Contents.base_content import BaseContent
from DB.Models import CarModel, CarQueryResponseModel


class CarContent(BaseContent):
    data: CarModel


class CarsContent(BaseContent):
    data: CarQueryResponseModel
