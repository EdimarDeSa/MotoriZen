from typing import Literal

from pydantic import BaseModel
from typing_extensions import TypedDict

HealthStatusType = Literal["Ok", "Error"]


class HealthStatus(TypedDict):
    status: HealthStatusType
    message: str | dict[str, str] | None


class HealthModel(BaseModel):
    status: HealthStatusType
    cache_status: HealthStatus
    database_status: HealthStatus
    auth_provider_status: HealthStatus
