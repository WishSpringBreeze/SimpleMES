# routers/product.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from database import get_session
from models import Product
from schemas import ProductBase, ProductCreate, ProductRead
from crud import create_item, get_item, get_items, get_item_by_field, update_item, delete_item

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(*, session: Session = Depends(get_session), product_in: ProductCreate):
    """
    创建一个新的产品。
    """
    # 检查 SKU 是否已存在
    existing_product = get_item_by_field(session, Product, "sku", product_in.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product_in.sku}' already exists."
        )
    return create_item(session, Product, product_in)

@router.get("/", response_model=List[ProductRead])
def read_products(*, session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    """
    获取产品列表。
    """
    return get_items(session, Product, offset, limit)

@router.get("/{product_id}", response_model=ProductRead)
def read_product(*, session: Session = Depends(get_session), product_id: int):
    """
    根据 ID 获取单个产品的详细信息。
    """
    product = get_item(session, Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(*, session: Session = Depends(get_session), product_id: int, product_in: ProductCreate):
    """
    根据 ID 更新一个产品的信息。
    """
    # 检查 SKU 更新后是否与其他产品冲突
    existing_product_with_new_sku = get_item_by_field(session, Product, "sku", product_in.sku)
    if existing_product_with_new_sku and existing_product_with_new_sku.id != product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Another product with SKU '{product_in.sku}' already exists."
        )
        
    updated_product = update_item(session, Product, product_id, product_in)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(*, session: Session = Depends(get_session), product_id: int):
    """
    根据 ID 删除一个产品。
    """
    deleted = delete_item(session, Product, product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    # 成功删除后返回 204 No Content，不需要返回 body