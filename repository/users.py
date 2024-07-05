from sqlalchemy.orm import Session
from schemas import users
from models import User
from passlib.context import CryptContext
from core.config import Role

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return password_context.hash(password)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create(db: Session, user: users.UserCreate):
    is_librarian = True if user.role == Role.LIBRARIAN else False
    db_user = User(
        email=user.email,
        name=user.name,
        role=user.role,
        is_librarian=is_librarian,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
