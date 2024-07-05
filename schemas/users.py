from pydantic import BaseModel, EmailStr
from core.config import Role

class User(BaseModel):
    name: str
    email: EmailStr


class UserCreate(User):
    password: str
    role: Role


class UserResponse(User):
    id: int
    is_active: bool
    is_librarian: bool

    class Config:
        orm_mode = True
