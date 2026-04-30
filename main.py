from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

# リハビリで作ったデータ
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]

# リハビリで作った関数を「Web用」に少し調整
@app.get("/users/{parity}")
def get_users(parity: int):
    """
    URLの末尾が /users/0 なら偶数、/users/1 なら奇数のユーザーを返す
    """
    if parity == 0:
        return [user for user in users if user['id'] % 2 == 0]
    else:
        return [user for user in users if user['id'] % 2 != 0]
    
@app.post("/users")
def creat_user(user: User):
    users.append(user.dict())
    return {"message": "ユーザーを登録しました", "user": user}

# 起動コマンド（ターミナルで実行）: uvicorn main:app --reload