from enum import Enum
from sqlmodel import Field
from core.base_model import BaseModel

class Product(BaseModel, table=True):
    product_type: str
