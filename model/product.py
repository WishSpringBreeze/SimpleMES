from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from core.base_model import BaseModel



class Product(BaseModel, table=True):
    product_type: str
    attributes: list["ProductAttribute"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class ProductAttribute(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    name: str
    value: str
    product: Optional[Product] = Relationship(back_populates="attributes")


from sqlalchemy import event

@event.listens_for(ProductAttribute, "before_update", propagate=True)
def bump_product_version_on_attribute_update(mapper, connection, target):
    if target.product:
        target.product.version_id += 1


@event.listens_for(ProductAttribute, "before_insert", propagate=True)
def bump_product_version_on_attribute_insert(mapper, connection, target):
    if target.product:
        target.product.version_id += 1


@event.listens_for(ProductAttribute, "before_delete", propagate=True)
def bump_product_version_on_attribute_delete(mapper, connection, target):
    if target.product:
        target.product.version_id += 1
