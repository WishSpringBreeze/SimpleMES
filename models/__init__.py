# models/__init__.py

# 从当前包的 product 模块中，导入 Product 类
from .product import Product

# (可选但推荐) 定义一个 __all__ 列表
# 这明确指出了当使用 `from models import *` 时，哪些名字是可以被导入的。
# 它能让代码更健壮，避免意外导入不必要的东西。
__all__ = [
    "Product",
]