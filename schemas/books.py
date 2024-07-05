from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    title: str
    author: str
    genre: str


class BookCreate(Book):
    pass

class BookResponse(Book):
    id: int
    available: bool
    owner_id: Optional[int]

    class Config:
        orm_mode = True
