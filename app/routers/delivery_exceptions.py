from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.delivery_exception import (
    DeliveryExceptionCreate,
    DeliveryExceptionResponse,DeliveryExceptionDetailResponse,DeliveryExceptionListResponse,
    DeliveryExceptionUpdate
)

from app.services import delivery_exception_service

from app.exceptions.customer_subscription_exceptions import (
    CustomerSubscriptionNotFoundError,
    InactiveCustomerSubscriptionError,
)

from app.exceptions.delivery_exception_exceptions import (
    InvalidDateRangeError,
    OverlappingDeliveryExceptionError,
    PastDateNotAllowedError,
    DeliveryExceptionNotFoundError
)

router = APIRouter(
    prefix="/delivery-exceptions",
    tags=["Delivery Exceptions"]
)


@router.post(
    "",
    response_model=DeliveryExceptionResponse,
    status_code=201
)
def create_delivery_exception(
        delivery_exception: DeliveryExceptionCreate,
        db: Session = Depends(get_db)
):

    try:
        return delivery_exception_service.create(
            db,
            delivery_exception
        )

    except CustomerSubscriptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InactiveCustomerSubscriptionError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except PastDateNotAllowedError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except InvalidDateRangeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except OverlappingDeliveryExceptionError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get(
    "",
    response_model=list[DeliveryExceptionListResponse]
)
def get_all_delivery_exceptions(
        db: Session = Depends(get_db)
):

    return delivery_exception_service.get_all(
        db
    )



@router.get(
    "/{delivery_exception_id}",
    response_model=DeliveryExceptionDetailResponse
)
def get_delivery_exception_by_id(
        delivery_exception_id: int,
        db: Session = Depends(get_db)
):

    try:
        return delivery_exception_service.get_by_id(
            db,
            delivery_exception_id
        )

    except DeliveryExceptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    

@router.put(
    "/{delivery_exception_id}",
    response_model=DeliveryExceptionResponse
)
def update_delivery_exception(
        delivery_exception_id: int,
        delivery_exception: DeliveryExceptionUpdate,
        db: Session = Depends(get_db)
):

    try:
        return delivery_exception_service.update_by_id(
            db,
            delivery_exception_id,
            delivery_exception
        )

    except DeliveryExceptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except PastDateNotAllowedError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except InvalidDateRangeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except OverlappingDeliveryExceptionError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.delete(
    "/{delivery_exception_id}",
    response_model=DeliveryExceptionResponse
)
def delete_delivery_exception(
        delivery_exception_id: int,
        db: Session = Depends(get_db)
):

    try:
        return delivery_exception_service.delete_by_id(
            db,
            delivery_exception_id
        )

    except DeliveryExceptionNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )