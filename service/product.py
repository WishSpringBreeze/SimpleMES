from core.base_service_modeling import BaseCreateService, BaseDeleteService, BaseUpdateService
from model.product import Product, ProductAttribute


class ProductCreateService(BaseCreateService):
    model_class = Product

    def post_create(self):
        attributes_data = self._relationship_data.get("attributes")
        if not attributes_data:
            return

        for attr in attributes_data:
            pa = ProductAttribute(
                product_id=self.model.id,
                name=attr.name,
                value=attr.value
            )
            self.session.add(pa)

class ProductUpdateService(BaseUpdateService):
    model_class = Product

    def post_update(self):
        attrs = self._relationship_data.get("attributes")
        if attrs is None:
            return

        # Map existing attributes by ID
        existing = {a.id: a for a in self.model.attributes}

        # IDs coming from the client
        incoming_ids = {
            a.id for a in attrs
            if getattr(a, "id", None) is not None
        }

        # 1. DELETE attributes missing from incoming list
        for attr_id, attr in existing.items():
            if attr_id not in incoming_ids:
                self.session.delete(attr)

        # 2. ADD or UPDATE attributes
        for attr_data in attrs:
            if getattr(attr_data, "id", None):
                # UPDATE existing attribute
                attr = existing[attr_data.id]
                attr.name = attr_data.name
                attr.value = attr_data.value
            else:
                # CREATE new attribute
                new_attr = ProductAttribute(
                    product_id=self.model.id,
                    name=attr_data.name,
                    value=attr_data.value
                )
                self.session.add(new_attr)

class ProductDeleteService(BaseDeleteService):
    model_class = Product

    def post_delete(self):
        """
        Override if you need domain-specific delete logic.
        For now, cascade delete handles ProductAttribute automatically.
        """
        pass
