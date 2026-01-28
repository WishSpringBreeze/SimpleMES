# models/subentity.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Subentity(SQLModel, table=False): # <-- 关键修正：table=False
    """
    所有子实体表的通用基础模型 (抽象基类)。
    这个类本身不对应任何数据库表。
    """
    # 主键 id 是通用的
    id: Optional[int] = Field(default=None, primary_key=True, index=True)