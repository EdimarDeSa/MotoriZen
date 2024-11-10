import uuid
from datetime import date
from typing import Optional, Sequence

from pydantic import BaseModel, Field

from DB.Models.range_model import RangeModel
from Enums import AggregationIntervalEnum, ReportsEnum


class ReportsQueryModel(BaseModel):
    reports: Optional[Sequence[ReportsEnum]] = Field(
        default=None,
        description="Reports to be returned, check Reports<type>Enum above. Can be multiple. If not provided, all reports will be returned.",
        examples=[
            [
                ReportsEnum.TOTAL_CONSUMPTION,
                ReportsEnum.MEAN_CONSUMPTION_PER_DISTANCE,
                ReportsEnum.MEAN_CONSUMPTION_PER_TRIP,
            ]
        ],
    )
    car_ids: Optional[Sequence[uuid.UUID]] = Field(
        default=None,
        description="Car ids to be returned. If not provided, all cars will be returned.",
    )
    time_frame: Optional[RangeModel[date]] = Field(
        default=None,
        description="Time range to search for reports. If not provided, current week will be used. Week starts on Monday.",
    )

    aggregation_interval: Optional[AggregationIntervalEnum] = Field(
        default=None,
        description="Aggregation interval for reports. If not provided, reports will not be aggregated.",
    )
