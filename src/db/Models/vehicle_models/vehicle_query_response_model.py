from db.Models import VehicleModel
from db.Models.base_query_response_model import BaseQueryResponseModel


class CarQueryResponseModel(BaseQueryResponseModel[VehicleModel]):
    pass
