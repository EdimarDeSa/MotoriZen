from pydantic import BaseModel, Field

from Utils.custom_primitive_types import PerPageOptions, SortOrderOptions, T


class BaseQueryMetadataModel(BaseModel):
    sort_by: str = Field(description="Field to sort by")
    sort_order: SortOrderOptions = Field(description="Order of sorting. asc for ascending and desc for descending")

    page: int = Field(description="Actual page number")
    per_page: PerPageOptions = Field(description="Number of records per page")
    total_pages: int = Field(description="Total pages")

    first_index: int = Field(description="First index of the query")
    last_index: int = Field(description="Last index of the query")
    total_results: int = Field(description="Total results existent in the database for the given filter")
