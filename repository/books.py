from sqlalchemy.orm import Session
from schemas import books
from models import Book
from fastapi import HTTPException


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def create(db: Session, book: books.BookCreate, user_id: int):
    db_book = Book(**book.model_dump(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def update(db: Session, book_id: int, book_update: books.BookCreate):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        for key, value in book_update.model_dump().items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return book
    raise HTTPException(status_code=404, detail="Book not found")


def delete(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return book
    raise HTTPException(status_code=404, detail="Book not found")
