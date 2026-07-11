from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_subscription import CustomerSubscription
from app.models.milk_type import MilkType
from app.models.route import Route

from app.schemas.customer_subscription import CustomerSubscriptionCreate
from app.schemas.customer_subscription import (
    CustomerSubscriptionListResponse,CustomerSubscriptionUpdate
)

from app.schemas.customer import CustomerSummaryResponse

from app.schemas.milk_type import MilkTypeSummaryResponse

from app.schemas.customer_subscription import (
    CustomerSubscriptionDetailResponse
)

from app.exceptions.customer_subscription_exceptions import (
    CustomerSubscriptionNotFoundError,DuplicateSubscriptionError
)

from app.exceptions.customer import (
    CustomerNotFoundError,
    InactiveCustomerError
)

from app.exceptions.milk_type_exceptions import (
    MilkTypeNotFoundError,
    InactiveMilkTypeError
)


from app.services import customer_service
from app.services import milk_type_service

def create(
    db: Session,
    subscription: CustomerSubscriptionCreate
) -> CustomerSubscription:
    
    customer = customer_service.get_by_id_internal(
        db,
        subscription.customer_id
    )

     
    milk_type = milk_type_service.get_by_id_internal(
        db,
        subscription.milk_type_id
    )

    existing_subscription = (
    db.query(CustomerSubscription)
    .filter(
        CustomerSubscription.customer_id == subscription.customer_id,
        CustomerSubscription.milk_type_id == subscription.milk_type_id,
        CustomerSubscription.shift == subscription.shift,
        CustomerSubscription.is_active == True
    )
    .first()
)

    if existing_subscription:
        raise DuplicateSubscriptionError()
    
    inactive_subscription = (
    db.query(CustomerSubscription)
    .filter(
        CustomerSubscription.customer_id == subscription.customer_id,
        CustomerSubscription.milk_type_id == subscription.milk_type_id,
        CustomerSubscription.shift == subscription.shift,
        CustomerSubscription.is_active == False
    )
    .first()
)

    inactive_subscription = (
        db.query(CustomerSubscription)
        .filter(
            CustomerSubscription.customer_id == subscription.customer_id,
            CustomerSubscription.milk_type_id == subscription.milk_type_id,
            CustomerSubscription.shift == subscription.shift,
            CustomerSubscription.is_active == False
        )
        .first()
    )

    if inactive_subscription:

        inactive_subscription.is_active = True
        inactive_subscription.quantity = subscription.quantity

        db.commit()
        db.refresh(inactive_subscription)

        return inactive_subscription
    
    new_subscription = CustomerSubscription(
        customer_id=subscription.customer_id,
        milk_type_id=subscription.milk_type_id,
        shift=subscription.shift,
        quantity=subscription.quantity
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription

def get_all(
        db: Session
) -> list[CustomerSubscriptionListResponse]:

    subscriptions = (
        db.query(
            CustomerSubscription.id,
            Customer.customer_code,
            Customer.customer_name,
            Route.route_name,
            MilkType.name.label("milk_type"),
            CustomerSubscription.shift,
            CustomerSubscription.quantity,
            CustomerSubscription.is_active
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
            CustomerSubscription.is_active == True
        )
        .order_by(
            Route.route_name,
            Customer.customer_name,
            CustomerSubscription.shift,
            MilkType.quantity_ml
        )
        .all()
    )

    return [
        CustomerSubscriptionListResponse(
            id=row.id,
            customer_code=row.customer_code,
            customer_name=row.customer_name,
            route_name=row.route_name,
            milk_type=row.milk_type,
            shift=row.shift,
            quantity=row.quantity,
            is_active=row.is_active
        )
        for row in subscriptions
    ]


def get_by_id(
        db: Session,
        subscription_id: int
) -> CustomerSubscriptionDetailResponse:

    subscription = (
        db.query(CustomerSubscription)
        .join(
            Customer,
            Customer.id == CustomerSubscription.customer_id
        )
        .join(
            MilkType,
            MilkType.id == CustomerSubscription.milk_type_id
        )
        .filter(
            CustomerSubscription.id == subscription_id,
            CustomerSubscription.is_active == True
        )
        .first()
    )

    if not subscription:
        raise CustomerSubscriptionNotFoundError()

    return CustomerSubscriptionDetailResponse(
        id=subscription.id,
        customer=CustomerSummaryResponse(
            id=subscription.customer.id,
            customer_code=subscription.customer.customer_code,
            customer_name=subscription.customer.customer_name
        ),
        milk_type=MilkTypeSummaryResponse(
            id=subscription.milk_type.id,
            name=subscription.milk_type.name,
            quantity_ml=subscription.milk_type.quantity_ml
        ),
        shift=subscription.shift,
        quantity=subscription.quantity,
        is_active=subscription.is_active,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at
    )

def update_by_id(
        db: Session,
        subscription_id: int,
        subscription: CustomerSubscriptionUpdate
) -> CustomerSubscription:

    existing_subscription = (
        db.query(CustomerSubscription)
        .filter(
            CustomerSubscription.id == subscription_id,
            CustomerSubscription.is_active == True
        )
        .first()
    )

    if not existing_subscription:
        raise CustomerSubscriptionNotFoundError()

    existing_subscription.quantity = subscription.quantity

    db.commit()
    db.refresh(existing_subscription)

    return existing_subscription

def delete_by_id(
        db: Session,
        subscription_id: int
) -> CustomerSubscription:

    existing_subscription = (
        db.query(CustomerSubscription)
        .filter(
            CustomerSubscription.id == subscription_id,
            CustomerSubscription.is_active == True
        )
        .first()
    )

    if not existing_subscription:
        raise CustomerSubscriptionNotFoundError()

    existing_subscription.is_active = False

    db.commit()
    db.refresh(existing_subscription)

    return existing_subscription