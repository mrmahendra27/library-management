import uvicorn
from fastapi import FastAPI
from core.database import Base, engine
from models import User, Book
from routers import books, users

User.metadata.create_all(bind=engine)
Book.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)


@app.get("/")
def home():
    return {"message": "Welcome to the Library Management System"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)