from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# 注意：这里的 DATABASE_URL 是示例，稍后我们会连接到你的 Server 2012
# 现在先用 SQLite 让程序跑起来
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mes_database.db")
print(f"Using database: {DATABASE_URL}") # 可选：打印出来确认加载成功

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)