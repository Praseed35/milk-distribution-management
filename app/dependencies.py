from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()