# models/base.py (正确)
from sqlmodel import SQLModel, Field
from typing import Optional

class BaseModel(SQLModel, table=False): # <-- 关键修正：table=False
    """
    所有数据库表的通用基础模型 (抽象基类)。
    这个类本身不对应任何数据库表。
    """
    # 因为 table=False，所以我们在这里定义字段时，通常不会给它们默认值，
    # 而是让子类来决定是否覆盖以及如何覆盖。
    # 但如果希望它们是通用的，可以提供默认值。
    
    # 主键 id 是通用的
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    # name 和 change_count 作为通用字段，提供默认行为
    name: str = Field(index=True)
    # 设为 Optional 并提供 None 默认值，因为不是所有子类都必须用它作为名称
    # 例如 BOMItem 的名称就是其物料的名称
    description: Optional[str] = None
    
    change_count: int = Field(default=1, nullable=False, description="Version number for optimistic locking")
    # change_count 可以给一个非空的默认值 1

    # 注意：绝对不要在这里定义 __tablename__