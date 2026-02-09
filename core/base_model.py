from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Integer
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    lastchangedate: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    version_id: int = Field(
        default=1,
        sa_column=Column(Integer, nullable=False)
    )






from sqlalchemy import event
@event.listens_for(BaseModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    target.version_id += 1
