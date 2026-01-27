# schemas/__init__.py

# 从当前包的 product 模块中，导入所有需要的 Schema 类
from .product import ProductBase, ProductCreate, ProductRead

# (强烈推荐) 定义 __all__ 列表，明确包的公有接口
__all__ = [
    "ProductBase", 
    "ProductCreate", 
    "ProductRead",
]