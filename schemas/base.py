# schemas/BOM.py
from sqlmodel import SQLModel
from typing import List, Optional

from models.base import BaseModel

# 注意：我们从 models.BOM 导入 ORM 模型，主要是为了在关系中使用
# 但在 schema 定义中通常不直接引用，这里只是示意其关联性
# from ..models.BOM import BOM 

class BaseSchema(BaseModel):
    name: str
    description: Optional[str] = None

class BaseCreate(BaseSchema):
    pass

class BaseRead(BaseSchema):
    id: int
    class Config:
        orm_mode = True

class BaseUpdate(BaseSchema):
    # 更新时，客户端必须提供他们上次读取到的 change_count
    change_count: int