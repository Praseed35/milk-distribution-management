# app/main.py

from fastapi import FastAPI

from app.database import engine
from app.models.user import User
from app.models.employee import Employee
from app.database import Base
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router

app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Milk Management API"
    }