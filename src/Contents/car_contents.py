from Contents.base_content import BaseContent
from db.Models.car_model import CarModel, CarsQueryResponseModel


class CarContent(BaseContent):
    data: CarModel


class CarsContent(BaseContent):
    data: CarsQueryResponseModel
