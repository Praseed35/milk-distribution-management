from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user import UserCreate

from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    return user_service.get_all(db)

@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = user_service.create(
        db,
        user
    )

    if new_user is None:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return new_user