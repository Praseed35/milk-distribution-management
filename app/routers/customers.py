from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate
)

from app.services import customer_service

from app.exceptions.customer import (
    DuplicatePrimaryPhoneError,
    SamePhoneNumberError,CustomerNotFoundError
)

from app.exceptions.route import (
    RouteNotFoundError,
    InactiveRouteError
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    try:

        return customer_service.create(
            db,
            customer
        )

    except RouteNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InactiveRouteError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except SamePhoneNumberError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except DuplicatePrimaryPhoneError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_all_customers(
    db:Session=Depends(get_db)
):
    return customer_service.get_all(
        db
        )

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer_by_id(
    customer_id:int,
    db:Session=Depends(get_db)
    
):
    try:
        return customer_service.get_by_id(
            db,
            customer_id)
    except CustomerNotFoundError as e:
         raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer_by_id(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    try:
        return customer_service.update_by_id(
            db,
            customer_id,
            customer
        )

    except CustomerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except RouteNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InactiveRouteError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except SamePhoneNumberError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except DuplicatePrimaryPhoneError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.delete(
    "/{customer_id}",
    response_model=CustomerResponse
)
def delete_customer_by_id(
    customer_id:int,
    db:Session=Depends(get_db)
):
    try:
        return customer_service.delete_by_id(
            db,
            customer_id
        )
    except CustomerNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )