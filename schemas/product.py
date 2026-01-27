# schemas/product.py
from sqlmodel import SQLModel
from typing import List, Optional

# 注意：我们从 models.product 导入 ORM 模型，主要是为了在关系中使用
# 但在 schema 定义中通常不直接引用，这里只是示意其关联性
# from ..models.product import Product 

class ProductBase(SQLModel):
    name: str
    sku: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    # work_orders: List[WorkOrderRead] = [] # 如果需要嵌套返回，可以在这里定义

    class Config:
        orm_mode = True