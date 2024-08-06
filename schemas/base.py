from pydantic import BaseModel


class BaseComplaint(BaseModel):
    title: str
    description: str
    amount: float


class UserBase(BaseModel):
    email: str
