from fastapi import APIRouter
from orchestrator.product import ProductOrchestrator
from schema.product import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductRead)
def create_product(data: ProductCreate):
    orchestrator = ProductOrchestrator()
    return orchestrator.run(data)
