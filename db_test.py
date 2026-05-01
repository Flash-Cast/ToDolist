import sqlite3

# 1. データベースに接続（test.db というファイルが作られます）
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 2. テーブルを作る（SQL命令）
# 「usersテーブルがなければ、idとnameという列で作ってね」という命令
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# 3. データを追加する（INSERT）
cursor.execute('INSERT INTO users (id, name) VALUES (10, "Takahashi")')

# 4. 変更を保存する
conn.commit()

# 5. データを取得して表示する（SELECT）
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

for row in rows:
    print(f"取得したデータ: {row}")

# 6. 接続を閉じる
conn.close()