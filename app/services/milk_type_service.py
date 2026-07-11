from sqlalchemy.orm import Session

from app.exceptions.milk_type_exceptions import DuplicateMilkTypeNameError
from app.exceptions.milk_type_exceptions import DuplicateQuantityError
from app.exceptions.milk_type_exceptions import MilkTypeNotFoundError,InactiveMilkTypeError
from app.models.milk_type import MilkType
from app.schemas.milk_type import MilkTypeCreate
from app.schemas.milk_type import MilkTypeUpdate

def create(
        db:Session,
        milk_type:MilkTypeCreate
)->MilkType:
    
    existing_milk_type=(
        db.query(MilkType)
        .filter(
            MilkType.name==milk_type.name
        )
        .first()
    )

    if existing_milk_type:
        raise DuplicateMilkTypeNameError(
            milk_type.name
        )
    
    existing_quantity=(
        db.query(MilkType)
        .filter(
            MilkType.quantity_ml==milk_type.quantity_ml
        )
        .first()
    )

    if existing_quantity:
        raise DuplicateQuantityError(
            milk_type.quantity_ml
        )
    
    new_milk_type=MilkType(
        name=milk_type.name,
        quantity_ml=milk_type.quantity_ml,
        description=milk_type.description
    )

    db.add(new_milk_type)
    db.commit()
    db.refresh(new_milk_type)

    return new_milk_type

def get_all(
        db:Session
)->list[MilkType]:
    
    milk_types = (
    db.query(MilkType)
    .filter(
        MilkType.is_active == True
    )
    .order_by(
        MilkType.quantity_ml
    )
    .all()
)
    return milk_types

def get_by_id(
        db:Session,
        milk_type_id:int
)->MilkType:
    
    milk_type=(
        db.query(MilkType)
        .filter(
            MilkType.id==milk_type_id,
            MilkType.is_active==True
        )
        .first()
    )

    if not milk_type:
        raise MilkTypeNotFoundError()
    
    return milk_type

def update_by_id(
        db:Session,
        milk_type_id:int,
        milk_type:MilkTypeUpdate
)->MilkType:
    
    update_to_milk_type=(
        db.query(MilkType)
        .filter(
            MilkType.id==milk_type_id,
            MilkType.is_active==True
        )
        .first()
    )

    if not update_to_milk_type:
        raise MilkTypeNotFoundError()
    
    existing_milk_type=(
        db.query(MilkType)
        .filter(
            MilkType.name==milk_type.name,
            MilkType.id!=milk_type_id
        )
        .first()
    )

    if existing_milk_type:
        raise DuplicateMilkTypeNameError(
            milk_type.name
        )
    
    update_to_milk_type.name=milk_type.name
    update_to_milk_type.description=milk_type.description

    db.commit()
    db.refresh(update_to_milk_type)

    return update_to_milk_type

def delete_by_id(
        db:Session,
        milk_type_id:int
)->MilkType:
    
    existing_milk_type=(
        db.query(MilkType)
        .filter(
            MilkType.id==milk_type_id,
            MilkType.is_active==True
        )
        .first()
    )

    if not existing_milk_type:
        raise MilkTypeNotFoundError()
    
    existing_milk_type.is_active=False

    db.commit()
    db.refresh(existing_milk_type)

    return existing_milk_type


def get_by_id_internal(
        db: Session,
        milk_type_id: int
) -> MilkType:

    milk_type = (
        db.query(MilkType)
        .filter(
            MilkType.id == milk_type_id
        )
        .first()
    )

    if not milk_type:
        raise MilkTypeNotFoundError()

    if not milk_type.is_active:
        raise InactiveMilkTypeError()

    return milk_type