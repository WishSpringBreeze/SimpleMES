from sqlmodel import SQLModel, Field, create_engine, Session

from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    sku: str = Field(index=True, unique=True)
    description: Optional[str] = None
    price: float