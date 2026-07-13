from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.schemas.customer import CustomerSummaryResponse
from app.schemas.customer_subscription import CustomerSubscriptionResponse
from app.schemas.milk_type import MilkTypeSummaryResponse
from app.constants.shifts import Shift


class DeliveryExceptionBase(BaseModel):

    customer_subscription_id: int = Field(
        ...,
        gt=0
    )

    start_date: date

    end_date: date

    quantity: int = Field(
        ...,
        ge=0
    )

    reason: str | None = Field(
        default=None,
        max_length=255
    )


class DeliveryExceptionCreate(DeliveryExceptionBase):
    pass


class DeliveryExceptionUpdate(BaseModel):

    start_date: date

    end_date: date

    quantity: int = Field(
        ...,
        ge=0
    )

    reason: str | None = Field(
        default=None,
        max_length=255
    )


class DeliveryExceptionResponse(DeliveryExceptionBase):

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DeliveryExceptionListResponse(BaseModel):

    id: int

    customer_code: str

    customer_name: str

    route_name: str

    milk_type: str

    shift: str

    start_date: date

    end_date: date

    quantity: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class DeliveryExceptionDetailResponse(BaseModel):

    id: int

    customer: CustomerSummaryResponse

    milk_type: MilkTypeSummaryResponse

    shift: Shift

    start_date: date

    end_date: date

    quantity: int

    reason: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )