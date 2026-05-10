from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# テンプレートの設定
templates = Jinja2Templates(directory="templates")

# DB設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_web.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DBモデル
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

# Pydanticモデル
class UserSchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True # orm_mode = True (Pydantic v2ではこちらが推奨)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---

@app.get("/users/{parity}")
def read_users(parity: int, db: Session = Depends(get_db)):
    all_users = db.query(UserDB).all()
    if parity == 0:
        return [u for u in all_users if u.id % 2 == 0]
    else:
        return [u for u in all_users if u.id % 2 != 0]

@app.post("/users")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = UserDB(id=user.id, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    target_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
    db.delete(target_user)
    db.commit()
    return {"message": "削除しました"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    target_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりませんでした")
    
    target_user.name = user.name
    db.commit()
    db.refresh(target_user)
    return target_user

# --- View Endpoint ---

@app.get("/view", response_class=HTMLResponse)
def read_users_view(request: Request, db: Session = Depends(get_db)):
    all_users = db.query(UserDB).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"users": all_users}
    )