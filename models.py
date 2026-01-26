from sqlmodel import SQLModel, Field
from typing import Optional

class WorkOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(index=True, unique=True)
    product_name: str
    quantity: int
    status: str = "Pending"

class ProductionReport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    work_order_id: int = Field(foreign_key="workorder.id")
    quantity_produced: int