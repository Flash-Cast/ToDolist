#1
names = ["Tanaka", "Sato", "Suzuki"]
for i, name in enumerate(names):
    # 補足メッセージを先に決める
    extra = "(長い名前)" if len(name) > 5 else ""
    # printは1回で済ませる
    print(f"{i}番目のユーザーは{name}です{extra}")

#2
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]
users.append({"id": 4, "name": "Takahashi"})

for user in users:
    # 'users'（リスト全体）ではなく 'user'（現在の辞書）を参照し、
    # ドット '.' ではなく '[]' でキーを指定します。
    print(f"ID: {user['id']} のユーザーは {user['name']} です")

#3
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]
users.append({"id": 4, "name": "Takahashi"})

for user in users:
    # 偶数判定を標準的な if 文で書く（可読性が高い）
    if user['id'] % 2 == 0:
        print(f"ID:{user['id']}のユーザーは{user['name']}です")

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
        # 辞書から名前(SatoやTakahashi)だけを抜き出してリストに追加
        even_user_names.append(user['name']) 

# リスト全体をそのまま表示
print(even_user_names)

#4.1
users = [
    {"id": 1, "name": "Tanaka"},
    {"id": 2, "name": "Sato"},
    {"id": 3, "name": "Suzuki"}
]
users.append({"id": 4, "name": "Takahashi"})
# [「追加したいもの」 for 「変数」 in 「リスト」 if 「条件」]
even_user_names = [user['name'] for user in users if user['id'] % 2 == 0]

print(even_user_names)  # ['Sato', 'Takahashi']

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