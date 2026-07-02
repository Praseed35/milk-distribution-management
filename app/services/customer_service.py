from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.route import Route

from app.schemas.customer import CustomerCreate,CustomerResponse,CustomerUpdate

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

def get_all(
    db: Session
) -> list[Customer]:
    
    customers = (
    db.query(Customer)
    .filter(
        Customer.is_active == True
    )
    .all()
)

    return customers

def get_by_id(
        db:Session,
        customer_id:int
)->Customer:
    
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.is_active == True
        )
        .first()
)

    if not customer:
        raise CustomerNotFoundError()

    return customer

def update_by_id(
        db:Session,
        customer_id:int,
        customer:CustomerUpdate
)->Customer:
    
    customer_to_update = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.is_active == True
        )
        .first()
)

    if not customer_to_update:
        raise CustomerNotFoundError()
    
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
            Customer.primary_phone==customer.primary_phone,
            Customer.id != customer_id
        )
        .first()
    )
    if existing_customer:
        raise DuplicatePrimaryPhoneError(
            customer.primary_phone
            )
    
    customer_to_update.customer_name = customer.customer_name
    customer_to_update.primary_phone = customer.primary_phone
    customer_to_update.alternate_phone = customer.alternate_phone
    customer_to_update.address = customer.address
    customer_to_update.route_id = customer.route_id
    customer_to_update.remarks = customer.remarks
    

    db.commit()
    db.refresh(customer_to_update)

    return customer_to_update

def delete_by_id(
    db: Session,
    customer_id: int
) -> Customer:

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.is_active == True
        )
        .first()
)

    if not customer:
        raise CustomerNotFoundError()
    
    customer.is_active=False

    db.commit()
    db.refresh(customer)

    return customer