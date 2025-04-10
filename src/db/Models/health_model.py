from pydantic import BaseModel

from Utils.custom_primitive_types import HealthStatusType
from Utils.custom_types import HealthStatus


class HealthModel(BaseModel):
    status: HealthStatusType
    cache_status: HealthStatus
    database_status: HealthStatus
    auth_provider_status: HealthStatus
