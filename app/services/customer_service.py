from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.route import Route

from app.schemas.customer import CustomerCreate

from app.exceptions.customer import (
    DuplicatePrimaryPhoneError,
    CustomerNotFoundError,
    SamePhoneNumberError
)

from app.exceptions.route import (
    RouteNotFoundError,
    InactiveRouteError
)

def create(
        db:Session,
        customer:CustomerCreate
)->Customer:
    
    existing_route = (
        db.query(Route)
        .filter(
            Route.id == customer.route_id
        )
        .first()
    )

    if not existing_route:
        raise RouteNotFoundError()
    
    if not existing_route.is_active:
        raise InactiveRouteError()
    
    if customer.primary_phone == customer.alternate_phone:
        raise SamePhoneNumberError()
    
    existing_customer=(
        db.query(Customer)
        .filter(
            Customer.primary_phone==customer.primary_phone
        ).first()
    )

    if existing_customer:
        raise DuplicatePrimaryPhoneError(
            customer.primary_phone
        )
    

    last_customer = (
    db.query(Customer)
    .order_by(Customer.id.desc())
    .first()
)

    if last_customer:
        next_number = int(last_customer.customer_code[1:]) + 1
    else:
        next_number = 1

    customer_code = f"C{next_number:05d}"

    new_customer = Customer(
        customer_code=customer_code,
        customer_name=customer.customer_name,
        primary_phone=customer.primary_phone,
        alternate_phone=customer.alternate_phone,
        address=customer.address,
        route_id=customer.route_id,
        remarks=customer.remarks
)

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer
