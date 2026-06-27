from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import LoginRequest

from app.core.security import (
    verify_password,
    create_access_token
)


def login(
    db: Session,
    login_data: LoginRequest
):

    user = (
        db.query(User)
        .filter(
            User.username == login_data.username
        )
        .first()
    )

    if not user:
        return None

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        return None

    access_token = create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return access_token