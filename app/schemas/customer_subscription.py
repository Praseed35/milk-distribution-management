from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.constants.shifts import Shift
from app.schemas.customer import CustomerSummaryResponse
from app.schemas.milk_type import MilkTypeSummaryResponse


class CustomerSubscriptionBase(BaseModel):

    customer_id: int = Field(
        ...,
        gt=0
    )

    milk_type_id: int = Field(
        ...,
        gt=0
    )

    shift: Shift

    quantity: int = Field(
        ...,
        gt=0
    )


class CustomerSubscriptionCreate(CustomerSubscriptionBase):
    pass


class CustomerSubscriptionUpdate(BaseModel):

    quantity: int = Field(
        ...,
        gt=0
    )


class CustomerSubscriptionResponse(CustomerSubscriptionBase):

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class CustomerSubscriptionListResponse(BaseModel):

    id: int

    customer_code: str

    customer_name: str

    route_name: str

    milk_type: str

    shift: Shift

    quantity: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
    
class CustomerSubscriptionDetailResponse(BaseModel):

    id: int

    customer: CustomerSummaryResponse

    milk_type: MilkTypeSummaryResponse

    shift: Shift

    quantity: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

