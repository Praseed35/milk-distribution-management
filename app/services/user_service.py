from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password


def get_all(db: Session):
    return db.query(User).all()


def create(db: Session, user):

    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:
        return None

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user