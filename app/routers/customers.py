from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse
)

from app.services import customer_service

from app.exceptions.customer import (
    DuplicatePrimaryPhoneError,
    SamePhoneNumberError
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