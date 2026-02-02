from core.base_orchestrator import OrchestratorBase
from service.product_service import ProductService

class ProductOrchestrator(OrchestratorBase):
    def __init__(self):
        super().__init__(ProductService)
