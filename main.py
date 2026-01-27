# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import create_db_and_tables, engine
from routers import products # 导入 products 路由器

app = FastAPI(title="Simple MES", version="0.1.0")

# CORS 配置，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 在生产环境中应替换为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含产品相关的路由
app.include_router(products.router)

# 应用启动时创建数据库表
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple MES API. Visit /docs for documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
