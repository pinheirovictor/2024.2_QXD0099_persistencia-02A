from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import User, SessionLocal, init_db

app = FastAPI()

# Inicializa o banco de dados
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post("/users/")
# def create_user(name: str, email: str, db: Session = Depends(get_db)):
#     user = User(name=name, email=email)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

@app.post("/users/")
def create_user(name: str, email: str, age: int, db: Session = Depends(get_db)):
    user = User(name=name, email=email, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()
