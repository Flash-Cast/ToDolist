#1
names = ["Tanaka", "Sato", "Suzuki"]
for i, name in enumerate(names):
    if len(name)<5:
        print(f"{i}番目のユーザーは{name}です")
    else:
       print(f"{i}番目のユーザーは{name}です(長い名前)")

#2
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]
users.append({"id": 4, "name": "Takahashi"})

for user in users:
    print(f"ID:{user["id"]}のユーザーは{user["name"]}です")

#3
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]
users.append({"id": 4, "name": "Takahashi"})

for user in users:
    print(f"ID:{user['id']}のユーザーは{user['name']}です") if user["id"] % 2 == 0 else ""

#4
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]
users.append({"id": 4, "name": "Takahashi"})

even_user_names = []

for user in users:
    if user["id"] % 2 == 0:
        even_user_names.append(user['name'])
print(even_user_names)       
    
#5
# 関数の定義（データの加工に集中する）
def get_names_by_id_parity(user_list, parity):
    # parity が 0 なら偶数、1 なら奇数のリストを作る
    if parity == 0:
        return [user['name'] for user in user_list if user['id'] % 2 == 0]
    else:
        return [user['name'] for user in user_list if user['id'] % 2 != 0]

# --- 以下、関数の外側（実行部分） ---

# 1. 元のデータを用意
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]

# 2. 新しいユーザーを追加（正しい辞書の追加方法）
new_id = int(input("追加するIDを入力してください: "))
new_name = input("追加する名前を入力してください: ")
users.append({"id": new_id, "name": new_name})

# 3. 関数を呼び出して結果を受け取る
even_names = get_names_by_id_parity(users, 0)
odd_names = get_names_by_id_parity(users, 1)

# 4. 結果を表示
print(f"偶数IDの人: {even_names}")
print(f"奇数IDの人: {odd_names}")