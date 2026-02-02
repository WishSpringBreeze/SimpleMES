from core.base_service import ServiceBase
from model.product import Product
from schema.product import ProductCreate

class ProductService(ServiceBase):

    def execute(self):
        self.model = Product(**self.input_data.dict())
