from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_web.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

class UserSchema(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True




app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{parity}")
def read_users(parity: int, db: Session = Depends(get_db)):
    all_users = db.query(UserDB).all()
    if parity == 0:
        return [u for u in all_users if u.id % 2 == 0]
    else:
        return [u for u in all_users if u.id % 2 != 0]
    
@app.post("/users")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = UserDB(id = user.id, name = user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

