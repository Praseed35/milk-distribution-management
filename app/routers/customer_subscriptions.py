from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.customer_subscription import (
    CustomerSubscriptionCreate,
    CustomerSubscriptionResponse,
)
from app.schemas.customer_subscription import (
    CustomerSubscriptionListResponse,CustomerSubscriptionDetailResponse,CustomerSubscriptionUpdate
)


from app.exceptions.customer_subscription_exceptions import (
    DuplicateSubscriptionError,CustomerSubscriptionNotFoundError
)
from app.services import customer_subscription_service

from app.exceptions.customer import (
    CustomerNotFoundError,
    InactiveCustomerError
)

from app.exceptions.milk_type_exceptions import (
    MilkTypeNotFoundError,
    InactiveMilkTypeError
)

router = APIRouter(
    prefix="/customer-subscriptions",
    tags=["Customer Subscriptions"]
)


@router.post(
    "",
    response_model=CustomerSubscriptionResponse
)
def create_customer_subscription(
    subscription: CustomerSubscriptionCreate,
    db: Session = Depends(get_db)
):
    try:
        return customer_subscription_service.create(
            db,
            subscription
        )

    except CustomerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InactiveCustomerError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except DuplicateSubscriptionError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except MilkTypeNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except InactiveMilkTypeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.get(
    "",
    response_model=list[CustomerSubscriptionListResponse]
)
def get_all_customer_subscriptions(
    db: Session = Depends(get_db)
):
    return customer_subscription_service.get_all(db)


@router.get(
    "/{subscription_id}",
    response_model=CustomerSubscriptionDetailResponse
)
def get_customer_subscription_by_id(
        subscription_id: int,
        db: Session = Depends(get_db)
):

    try:
        return customer_subscription_service.get_by_id(
            db,
            subscription_id
        )

    except CustomerSubscriptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
@router.put(
    "/{subscription_id}",
    response_model=CustomerSubscriptionResponse
)
def update_customer_subscription(
        subscription_id: int,
        subscription: CustomerSubscriptionUpdate,
        db: Session = Depends(get_db)
):

    try:
        return customer_subscription_service.update_by_id(
            db,
            subscription_id,
            subscription
        )

    except CustomerSubscriptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    

@router.delete(
    "/{subscription_id}",
    response_model=CustomerSubscriptionResponse
)
def delete_customer_subscription(
        subscription_id: int,
        db: Session = Depends(get_db)
):

    try:
        return customer_subscription_service.delete_by_id(
            db,
            subscription_id
        )

    except CustomerSubscriptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )