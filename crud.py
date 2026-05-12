from sqlalchemy.orm import Session
import models
import schemas

# 全ユーザー取得
def get_users(db: Session):
    return db.query(models.UserDB).all()

# ユーザー作成
def create_user(db: Session, user: schemas.UserSchema):
    db_user = models.UserDB(id=user.id, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー更新
def update_user(db: Session, user_id: int, user: schemas.UserSchema):
    target = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if target:
        target.name = user.name
        db.commit()
        db.refresh(target)
    return target

# ユーザー削除
def delete_user(db: Session, user_id: int):
    target = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if target:
        db.delete(target)
        db.commit()
        return True
    return False