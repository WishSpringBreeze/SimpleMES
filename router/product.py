from fastapi import APIRouter
from core.base_query import BaseQuery
from core.base_schema import BaseDelete
from orchestrator.product import (
    ProductCreateOrchestrator,
    ProductDeleteOrchestrator,
    ProductQueryOrchestrator,
    ProductUpdateOrchestrator
)
from schema.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/create", response_model=ProductRead)
def create_product(data: ProductCreate):
    orch = ProductCreateOrchestrator()
    return orch.run(data)


@router.get("/search", response_model=list[ProductRead])
def search_products(
    id: int | None = None,
    name: str | None = None,
    like: str | None = None
):
    query = BaseQuery(id=id, name=name, like=like)
    orch = ProductQueryOrchestrator()
    return orch.run(query)


@router.put("/update/{product_name}", response_model=ProductRead)
def update_product_by_name(product_name: str, data: ProductUpdate):
    # Inject the name into the update payload
    data.name = product_name
    orch = ProductUpdateOrchestrator()
    return orch.run(data)


@router.delete("/delete/{product_name}", response_model=bool)
def delete_product_by_name(product_name: str):
    payload = BaseDelete(name=product_name)
    orch = ProductDeleteOrchestrator()
    return orch.run(payload)
