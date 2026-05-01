from sqlalchemy import create_all, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 接続の設定（SQLiteを使用）
engine = create_engine('sqlite:///sample.db')
Base = declarative_base()

# 2. テーブルの定義（クラスとして書く！）
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# 初回のみ：テーブルを実際に作成する
Base.metadata.create_all(engine)

# 3. データベースを操作する「セッション」を作る
Session = sessionmaker(bind=engine)
session = Session()

# 4. データの追加（Pythonのオブジェクトを作る感覚）
new_user = User(id=100, name="Abe")
session.add(new_user)
session.commit() # 変更を確定！

# 5. データの取得
users = session.query(User).all()
for u in users:
    print(f"ID: {u.id}, Name: {u.name}")