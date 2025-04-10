from db.Models import CarModel
from db.Models.base_query_response_model import BaseQueryResponseModel


class CarQueryResponseModel(BaseQueryResponseModel[CarModel]):
    pass
