# models/bom.py
from typing import List, Optional
from sqlmodel import Field, Relationship
from .base import BaseModel

# BOM 继承 BaseModel 并声明 table=True
class BOM(BaseModel, table=True):
    version: str = Field(nullable=False) # 版本号