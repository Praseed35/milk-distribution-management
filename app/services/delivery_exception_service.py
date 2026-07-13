
from datetime import date

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.exceptions.delivery_exception_exceptions import (
    InvalidDateRangeError,
    OverlappingDeliveryExceptionError,
    PastDateNotAllowedError
)
from app.models.delivery_exception import DeliveryException
from app.schemas.delivery_exception import DeliveryExceptionCreate
from app.services import customer_subscription_service

from app.models.customer import Customer
from app.models.customer_subscription import CustomerSubscription
from app.models.delivery_exception import DeliveryException
from app.models.milk_type import MilkType
from app.models.route import Route

from app.schemas.delivery_exception import (
    DeliveryExceptionListResponse,DeliveryExceptionUpdate
)

from app.schemas.customer import CustomerSummaryResponse

from app.schemas.delivery_exception import (
    DeliveryExceptionDetailResponse
)

from app.schemas.milk_type import MilkTypeSummaryResponse

from app.exceptions.delivery_exception_exceptions import (
    DeliveryExceptionNotFoundError
)

def create(
        db: Session,
        delivery_exception: DeliveryExceptionCreate
) -> DeliveryException:

    customer_subscription_service.get_by_id_internal(
        db,
        delivery_exception.customer_subscription_id
    )

    if delivery_exception.start_date < date.today():
        raise PastDateNotAllowedError()

    if delivery_exception.end_date < delivery_exception.start_date:
        raise InvalidDateRangeError()

    overlapping_exception = (
        db.query(DeliveryException)
        .filter(
            DeliveryException.customer_subscription_id ==
            delivery_exception.customer_subscription_id,

            DeliveryException.is_active == True,

            and_(
                DeliveryException.start_date <= delivery_exception.end_date,
                DeliveryException.end_date >= delivery_exception.start_date
            )
        )
        .first()
    )

    if overlapping_exception:
        raise OverlappingDeliveryExceptionError()

    new_exception = DeliveryException(
        customer_subscription_id=delivery_exception.customer_subscription_id,
        start_date=delivery_exception.start_date,
        end_date=delivery_exception.end_date,
        quantity=delivery_exception.quantity,
        reason=delivery_exception.reason
    )

    db.add(new_exception)
    db.commit()
    db.refresh(new_exception)

    return new_exception



def get_all(
        db: Session
) -> list[DeliveryExceptionListResponse]:

    delivery_exceptions = (
        db.query(
            DeliveryException.id,
            Customer.customer_code,
            Customer.customer_name,
            Route.route_name,
            MilkType.name.label("milk_type"),
            CustomerSubscription.shift,
            DeliveryException.start_date,
            DeliveryException.end_date,
            DeliveryException.quantity,
            DeliveryException.is_active
        )
        .join(
            CustomerSubscription,
            CustomerSubscription.id == DeliveryException.customer_subscription_id
        )
        .join(
            Customer,
            Customer.id == CustomerSubscription.customer_id
        )
        .join(
            Route,
            Route.id == Customer.route_id
        )
        .join(
            MilkType,
            MilkType.id == CustomerSubscription.milk_type_id
        )
        .filter(
            DeliveryException.is_active == True
        )
        .order_by(
            DeliveryException.start_date,
            Route.route_name,
            Customer.customer_name,
            CustomerSubscription.shift,
            MilkType.quantity_ml
        )
        .all()
    )

    return [
        DeliveryExceptionListResponse(
            id=row.id,
            customer_code=row.customer_code,
            customer_name=row.customer_name,
            route_name=row.route_name,
            milk_type=row.milk_type,
            shift=row.shift,
            start_date=row.start_date,
            end_date=row.end_date,
            quantity=row.quantity,
            is_active=row.is_active
        )
        for row in delivery_exceptions
    ]


def get_by_id(
        db: Session,
        delivery_exception_id: int
) -> DeliveryExceptionDetailResponse:

    delivery_exception = (
        db.query(DeliveryException)
        .join(
            CustomerSubscription,
            CustomerSubscription.id == DeliveryException.customer_subscription_id
        )
        .join(
            Customer,
            Customer.id == CustomerSubscription.customer_id
        )
        .join(
            MilkType,
            MilkType.id == CustomerSubscription.milk_type_id
        )
        .filter(
            DeliveryException.id == delivery_exception_id,
            DeliveryException.is_active == True
        )
        .first()
    )

    if not delivery_exception:
        raise DeliveryExceptionNotFoundError()

    return DeliveryExceptionDetailResponse(
        id=delivery_exception.id,

        customer=CustomerSummaryResponse(
            id=delivery_exception.customer_subscription.customer.id,
            customer_code=delivery_exception.customer_subscription.customer.customer_code,
            customer_name=delivery_exception.customer_subscription.customer.customer_name
        ),

        milk_type=MilkTypeSummaryResponse(
            id=delivery_exception.customer_subscription.milk_type.id,
            name=delivery_exception.customer_subscription.milk_type.name,
            quantity_ml=delivery_exception.customer_subscription.milk_type.quantity_ml
        ),

        shift=delivery_exception.customer_subscription.shift,

        start_date=delivery_exception.start_date,
        end_date=delivery_exception.end_date,
        quantity=delivery_exception.quantity,
        reason=delivery_exception.reason,

        is_active=delivery_exception.is_active,
        created_at=delivery_exception.created_at,
        updated_at=delivery_exception.updated_at
    )


def update_by_id(
        db: Session,
        delivery_exception_id: int,
        delivery_exception: DeliveryExceptionUpdate
) -> DeliveryException:

    existing_delivery_exception = (
        db.query(DeliveryException)
        .filter(
            DeliveryException.id == delivery_exception_id,
            DeliveryException.is_active == True
        )
        .first()
    )

    if not existing_delivery_exception:
        raise DeliveryExceptionNotFoundError()

    if delivery_exception.start_date < date.today():
        raise PastDateNotAllowedError()

    if delivery_exception.end_date < delivery_exception.start_date:
        raise InvalidDateRangeError()

    overlapping_exception = (
        db.query(DeliveryException)
        .filter(
            DeliveryException.customer_subscription_id
            == existing_delivery_exception.customer_subscription_id,

            DeliveryException.id != delivery_exception_id,

            DeliveryException.is_active == True,

            and_(
                DeliveryException.start_date <= delivery_exception.end_date,
                DeliveryException.end_date >= delivery_exception.start_date
            )
        )
        .first()
    )

    if overlapping_exception:
        raise OverlappingDeliveryExceptionError()

    existing_delivery_exception.start_date = delivery_exception.start_date
    existing_delivery_exception.end_date = delivery_exception.end_date
    existing_delivery_exception.quantity = delivery_exception.quantity
    existing_delivery_exception.reason = delivery_exception.reason

    db.commit()
    db.refresh(existing_delivery_exception)

    return existing_delivery_exception

def delete_by_id(
        db: Session,
        delivery_exception_id: int
) -> DeliveryException:

    existing_delivery_exception = (
        db.query(DeliveryException)
        .filter(
            DeliveryException.id == delivery_exception_id,
            DeliveryException.is_active == True
        )
        .first()
    )

    if not existing_delivery_exception:
        raise DeliveryExceptionNotFoundError()

    existing_delivery_exception.is_active = False

    db.commit()
    db.refresh(existing_delivery_exception)

    return existing_delivery_exception