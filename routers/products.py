# routers/product.py
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session
from typing import List

from database import get_session
from models import Product
from schemas import ProductBase, ProductCreate, ProductRead
from crud import create_item, get_item, get_items, get_item_by_field, update_item, delete_item, update_item_with_version
from schemas.product import ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(*, session: Session = Depends(get_session), product_in: ProductCreate):
    """
    创建一个新的产品。
    """
    return create_item(session, Product, product_in)

@router.get("/", response_model=List[ProductRead])
def read_products(*, session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    """
    获取产品列表。
    """
    return get_items(session, Product, offset, limit)


@router.get("/{product_name}", response_model=ProductRead)
def read_product_by_name(*, session: Session = Depends(get_session), product_name: str = Path(..., title="The name of the product to retrieve")):
    """
    根据名称获取单个产品的详细信息。
    """
    product = get_item_by_field(session, Product, "name", product_name)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

# --- 新增：根据 Name 修改产品 ---
@router.put("/{product_name}", response_model=ProductRead)
def update_product_by_name(
    *, 
    session: Session = Depends(get_session), 
    product_name: str = Path(..., title="The name of the product to update"),
    product_in: ProductCreate
):
    """
    根据产品名称更新一个产品的信息。
    """
    # 1. 首先，根据名称查找产品
    product_to_update = get_item_by_field(session, Product, "name", product_name)
    if not product_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with name '{product_name}' not found")
    
    # 2. (可选但推荐) 检查新的名称是否与其他产品冲突
    # 如果用户想把产品A改名为产品B的名字，而产品B已存在，则会冲突
    if product_in.name != product_name:
        existing_product_with_new_name = get_item_by_field(session, Product, "name", product_in.name)
        if existing_product_with_new_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Another product with name '{product_in.name}' already exists."
            )

    # 3. 调用 CRUD 函数进行更新
    # update_item 需要产品的 ID，我们从 product_to_update 对象中获取
    updated_product = update_item(session, Product, product_to_update.id, product_in)
    
    # 由于 update_item 在未找到时会返回 None，但我们已提前检查过，所以这里理论上不会为 None
    # 但保留检查以策万全
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update product.")

    return updated_product

# --- 新增：根据 Name 删除产品 ---
@router.delete("/{product_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_name(
    *, 
    session: Session = Depends(get_session), 
    product_name: str = Path(..., title="The name of the product to delete") # 从路径中获取产品名称
):
    """
    根据产品名称删除一个产品。
    """
    # 1. 首先，根据名称查找产品以获取其 ID
    product_to_delete = get_item_by_field(session, Product, "name", product_name)
    if not product_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with name '{product_name}' not found")
    
    # 2. 调用 CRUD 函数进行删除
    # delete_item 需要产品的 ID，我们从 product_to_delete 对象中获取
    deleted = delete_item(session, Product, product_to_delete.id)
    
    # 如果 delete_item 返回 None (未找到)，但我们已提前检查过，所以这里理论上不会为 None
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete product.")
        
    # 成功删除后返回 204 No Content

# ... (@router.put("/{product_name}", ...) ...)
@router.put("/{product_name}", response_model=ProductRead)
def update_product_by_name(
    *, 
    session: Session = Depends(get_session), 
    product_name: str = Path(..., title="The name of the product to update"),
    product_in: ProductUpdate # 改为使用 ProductUpdate
):
    """
    根据产品名称更新一个产品的信息 (使用乐观锁防止并发冲突)。
    """
    product_to_update = get_item_by_field(session, Product, "name", product_name)
    if not product_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with name '{product_name}' not found")

    try:
        # 注意：我们传入的是从数据库查到的 product_to_update.id
        updated_product = update_item_with_version(session, Product, product_to_update.id, product_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    if not updated_product:
        # 版本冲突
        # 需要重新查询一次来获取最新的版本号以提示用户
        latest_product = get_item_by_field(session, Product, "name", product_name)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Product data conflict. The product was modified by another process. Please refresh and try again. Current version is {latest_product.version}."
        )
        
    return updated_product