from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.user import UserCreate
from app.models.user import User

from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    users=db.query(User).all()
    return users

@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
    db.query(User)
    .filter(
        User.username == user.username
    )
    .first()
)

    if existing_user:
        return {
        "message": "Username already exists"
    }
    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user