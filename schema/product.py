# schema/product_schema.py
from core.base_schema import BaseCreate, BaseRead, BaseUpdate

class ProductSchema():
    product_type: str

class ProductCreate(BaseCreate,ProductSchema):
    pass

class ProductUpdate(BaseUpdate,ProductSchema):
    pass

class ProductRead(BaseRead,ProductSchema):
    pass
