from pydantic import Field

from DB.Models.base_metadata_model import BaseMetadataModel
from Utils.custom_primitive_types import PerPageOptions, SortOrderOptions
from Utils.Internacionalization import ModelsDescriptionTexts


class BaseQueryMetadataModel(BaseMetadataModel):
    sort_by: str = Field(description=ModelsDescriptionTexts.SORT_BY)
    sort_order: SortOrderOptions = Field(description=ModelsDescriptionTexts.SORT_ORDER)

    page: int = Field(description=ModelsDescriptionTexts.PAGE)
    per_page: PerPageOptions = Field(description=ModelsDescriptionTexts.PER_PAGE)
    total_pages: int = Field(description=ModelsDescriptionTexts.TOTAL_PAGES)

    first_index: int = Field(description=ModelsDescriptionTexts.FIRST_INDEX)
    last_index: int = Field(description=ModelsDescriptionTexts.LAST_INDEX)

    total_results: int = Field(description=ModelsDescriptionTexts.TOTAL_RESULTS)
