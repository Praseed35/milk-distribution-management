from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class MilkTypeBase(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    quantity_ml: int = Field(
        ...,
        gt=0
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class MilkTypeCreate(MilkTypeBase):
    pass


class MilkTypeUpdate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class MilkTypeResponse(MilkTypeBase):

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class MilkTypeSummaryResponse(BaseModel):

    id: int

    name: str

    quantity_ml: int

    model_config = ConfigDict(
        from_attributes=True
    )