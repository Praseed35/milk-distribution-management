from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class RouteBase(BaseModel):

    route_code: str = Field(
        min_length=2,
        max_length=20
    )

    route_name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )


class RouteCreate(RouteBase):
    pass


class RouteUpdate(RouteBase):

    pass


class RouteResponse(RouteBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )