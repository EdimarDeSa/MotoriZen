import uuid
from datetime import date, time
from typing import Optional, Sequence, Union

from pydantic import BaseModel, Field

from DB.Models.range_model import RangeModel
from Enums import (
    ReportsDailyEnum,
    ReportsMeanEnum,
    ReportsMonthlyEnum,
    ReportsTotalEnum,
    ReportsWeeklyEnum,
    ReportsYearlyEnum,
)

ReportsType = Sequence[
    ReportsTotalEnum | ReportsMeanEnum | ReportsDailyEnum | ReportsWeeklyEnum | ReportsMonthlyEnum | ReportsYearlyEnum
]


class ReportsQueryModel(BaseModel):
    reports: Optional[ReportsType] = Field(
        default=None,
        description="Reports to be returned, check Reports<type>Enum above. Can be multiple. If not provided, all reports will be returned.",
        examples=[
            [
                ReportsTotalEnum.TOTAL_CONSUMPTION,
                ReportsMeanEnum.MEAN_CONSUMPTION_PER_DISTANCE,
                ReportsDailyEnum.DAILY_CONSUMPTION,
            ]
        ],
    )
    car_ids: Optional[Sequence[uuid.UUID]] = Field(
        default=None,
        description="Car ids to be returned. If not provided, all cars will be returned.",
    )
    date_: Optional[RangeModel[date]] = Field(
        default=None,
        description="Date of the trip. If not provided, current week will be used. Week starts on Monday.",
        alias="date",
    )
