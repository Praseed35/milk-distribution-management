from pydantic import BaseModel


class EmployeeCreate(BaseModel):

    name: str

    phone: str

    address: str

    user_id: int