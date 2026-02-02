from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class BaseCreate(SQLModel):
    name: str
    description: Optional[str] = None

class BaseUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class BaseRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    lastchangedate: datetime