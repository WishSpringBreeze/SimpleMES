from pydantic import BaseModel
from typing import Optional

class WorkOrderCreate(BaseModel):
    order_number: str
    product_name: str
    quantity: int

class WorkOrderRead(WorkOrderCreate):
    id: int
    status: str

    class Config:
        orm_mode = True