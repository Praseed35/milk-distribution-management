from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.dependencies import get_db
from app.schemas.auth import LoginRequest
from app.models.user import User
from app.core.auth import get_current_user
from app.core.roles import require_role

from app.core.security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.username == login_data.username
        )
        .first()
    )

    if not user:
        raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
)

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
        )

    access_token = create_access_token(
    {
        "sub": user.username,
        "role": user.role
    }
)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }

@router.get("/owner-dashboard")
def owner_dashboard(
    current_user = Depends(
        require_role(
            ["OWNER"]
        )
    )
):
    return {
        "message": "Welcome Owner"
    }