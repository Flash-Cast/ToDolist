from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# 作成したファイルをインポート
import models
import schemas
from database import engine, get_db

# DBテーブルの作成（起動時に実行）
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- 画面表示 ---
@app.get("/view", response_class=HTMLResponse)
def read_users_view(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.UserDB).all()
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"users": users}
    )

# --- API (作成・削除) ---
@app.post("/users", response_model=schemas.UserSchema)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = models.UserDB(id=user.id, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    target = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(target)
    db.commit()
    return {"message": "deleted"}