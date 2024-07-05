from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from repository.books import get_books, create, get_book, update, delete
from schemas.books import BookCreate, BookResponse
from core.database import get_db
from core.auth import get_current_active_librarian, get_current_active_user

router = APIRouter()


@router.post("/books/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_librarian),
):
    return create(db=db, book=book, user_id=current_user.id)


@router.get("/books/", response_model=list[BookResponse])
def read_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    books = get_books(db, skip=skip, limit=limit)
    return books


@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_librarian),
):
    return update(db=db, book_id=book_id, book_update=book)


@router.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_librarian),
):
    return delete(db=db, book_id=book_id)
