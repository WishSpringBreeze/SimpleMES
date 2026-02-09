from core.base_orchestrator import BaseOrchestrator
from core.base_service_query import BaseQueryService
from schema.product import ProductRead
from model.product import Product

from service.product import (
    ProductCreateService,
    ProductUpdateService,
    ProductDeleteService
)


class ProductQueryOrchestrator(BaseOrchestrator):
    def __init__(self):
        super().__init__(BaseQueryService, ProductRead)
        self.service_cls.model_class = Product


class ProductCreateOrchestrator(BaseOrchestrator):
    def __init__(self):
        super().__init__(ProductCreateService)
        self.service_cls.model_class = Product


class ProductUpdateOrchestrator(BaseOrchestrator):
    def __init__(self):
        super().__init__(ProductUpdateService)
        self.service_cls.model_class = Product


class ProductDeleteOrchestrator(BaseOrchestrator):
    def __init__(self):
        super().__init__(ProductDeleteService)
        self.service_cls.model_class = Product
