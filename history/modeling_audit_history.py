from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class ModelingAuditHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model_name: str
    model_id: int
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: str  # JSON snapshot
