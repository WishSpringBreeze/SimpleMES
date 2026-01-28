# schemas/bom.py
from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseSchema
from .product import ProductRead # 用于嵌套展示


class BOMRead(BaseSchema):
    version: int

class BOMCreate(BaseSchema):
    version: int