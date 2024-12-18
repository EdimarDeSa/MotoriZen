import uuid
from datetime import date
from typing import Optional, Sequence

from pydantic import BaseModel, Field

from DB.Models.range_model import RangeModel
from Enums import AggregationIntervalEnum, ReportsEnum
from Utils.Internacionalization import ModelsDescriptionTexts


class ReportsQueryModel(BaseModel):
    reports: Optional[Sequence[ReportsEnum]] = Field(
        default=None,
        description=ModelsDescriptionTexts.REPORTS,
        examples=[
            [
                ReportsEnum.TOTAL_CONSUPTION,
                ReportsEnum.MEAN_CONSUPTION_PER_DISTANCE,
                ReportsEnum.MEAN_CONSUPTION_PER_TRIP,
            ]
        ],
    )
    car_ids: Optional[Sequence[uuid.UUID]] = Field(
        default=None,
        description=ModelsDescriptionTexts.CAR_IDS,
    )
    time_frame: Optional[RangeModel[date]] = Field(
        default=None,
        description=ModelsDescriptionTexts.TIME_FRAME,
    )

    aggregation_interval: Optional[AggregationIntervalEnum] = Field(
        default=None,
        description=ModelsDescriptionTexts.AGGREGATION_INTERVAL,
    )
