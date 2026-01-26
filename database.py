from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# 注意：这里的 DATABASE_URL 是示例，稍后我们会连接到你的 Server 2012
# 现在先用 SQLite 让程序跑起来
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mes_test.db")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)