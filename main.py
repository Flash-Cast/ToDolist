from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# 作成したファイルをインポート
import models
import schemas
from database import engine, get_db
import crud

# DBテーブルの作成（起動時に実行）
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- 画面表示 ---
@app.get("/view", response_class=HTMLResponse)
def read_users_view(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"users": users}
    )

# --- API (作成・削除) ---
@app.post("/users", response_model=schemas.UserSchema)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.put("/users/{user_id}", response_model=schemas.UserSchema)
def update_user(user_id: int, user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "deleted"}