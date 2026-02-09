from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class BaseCreate(SQLModel):
    name: str
    description: Optional[str] = None

# class BaseUpdate(SQLModel):
#     name: Optional[str] = None
#     description: Optional[str] = None

class BaseRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    lastchangedate: datetime

from sqlmodel import SQLModel
from typing import Dict, Any

class BaseUpdate(SQLModel):
    id: int | None = None
    name: str | None = None
    data: Dict[str, Any]

# from typing import Generic, TypeVar
# from sqlmodel import SQLModel

# T = TypeVar("T", bound=SQLModel)

# class BaseUpdate(SQLModel, Generic[T]):
#     id: int | None = None
#     name: str | None = None
#     data: T


from sqlmodel import SQLModel

class BaseDelete(SQLModel):
    id: int | None = None
    name: str | None = None
