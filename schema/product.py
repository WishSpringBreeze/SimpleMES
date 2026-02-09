from sqlmodel import SQLModel
from core.base_schema import BaseCreate, BaseRead, BaseUpdate


class ProductAttributeBase(SQLModel):
    name: str
    value: str


class ProductAttributeCreate(ProductAttributeBase):
    pass


class ProductAttributeRead(ProductAttributeBase):
    id: int


class ProductSchema():
    product_type: str
    attributes: list[ProductAttributeCreate] = []

class ProductCreate(BaseCreate,ProductSchema):
    pass

class ProductUpdate(BaseUpdate, SQLModel):
    product_type: str | None = None
    attributes: list[ProductAttributeCreate | ProductAttributeRead] | None = None


class ProductRead(BaseRead, SQLModel):
    product_type: str
    attributes: list[ProductAttributeRead] = []

