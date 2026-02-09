from sqlmodel import Session
from history.modeling_audit_history import ModelingAuditHistory
import json
from core.base_service import BaseService
from sqlmodel import select


class BaseServiceModeling(BaseService):
    model_class = None
    def __init__(self, session: Session):
        super().__init__(session)
        self.modeling_action = None
        self._audit_snapshot = None   # for delete

    def initialize(self, data):
        self.data = data
        Model = self.model_class
        self._audit_snapshot = self.model.json() if hasattr(self, "model") and self.model else None

        # Auto-detect relationship fields
        self._relationship_fields = set(Model.__sqlmodel_relationships__.keys())

        # Extract relationship data for post_create/post_update
        self._relationship_data = {
            field: getattr(data, field, None)
            for field in self._relationship_fields
        }

    def _extract_non_relationship_data(self):
        """Return only simple fields (exclude relationship lists)."""
        return self.data.dict(
            exclude=self._relationship_fields,
            exclude_unset=True
        )

    def save(self):
        # First, let BaseService commit the main model
        super().save()

        # Ensure model has an ID before audit
        self.session.flush()

        # Write audit history
        if self.model:
            history = ModelingAuditHistory(
                model_name=self.model.__class__.__name__,
                model_id=self.model.id,
                action=self.modeling_action,
                data=self._audit_snapshot or self.model.json()
            )
            self.session.add(history)


class BaseCreateService(BaseServiceModeling):
    model_class = None

    def initialize(self, data):
        super().initialize(data)

        Model = self.model_class

        # Create parent model using only simple fields
        simple_data = self._extract_non_relationship_data()
        self.model = Model(**simple_data)

    def execute(self):
        super().execute()

        self.session.add(self.model)
        self.session.flush()  # parent ID now available

        self.post_create()

        self.modeling_action = "create"

    def post_create(self):
        pass



class BaseUpdateService(BaseServiceModeling):
    model_class = None

    def initialize(self, data):
        super().initialize(data)

        Model = self.model_class
        stmt = select(Model)

        if getattr(data, "id", None) is not None:
            stmt = stmt.where(Model.id == data.id)
        if getattr(data, "name", None) is not None:
            stmt = stmt.where(Model.name == data.name)

        obj = self.session.exec(stmt).first()
        if not obj:
            raise ValueError("Not found")

        self.model = obj

        # Capture snapshot BEFORE update
        self._audit_snapshot = obj.json()

        # Update simple fields only
        simple_data = self._extract_non_relationship_data()
        for field, value in simple_data.items():
            setattr(self.model, field, value)

    def execute(self):
        super().execute()

        # Child updates happen in subclass
        self.post_update()

        self.modeling_action = "update"

    def post_update(self):
        pass


class BaseDeleteService(BaseServiceModeling):
    model_class = None

    def initialize(self, data):
        super().initialize(data)

        Model = self.model_class
        stmt = select(Model)

        if getattr(data, "id", None) is not None:
            stmt = stmt.where(Model.id == data.id)
        if getattr(data, "name", None) is not None:
            stmt = stmt.where(Model.name == data.name)

        obj = self.session.exec(stmt).first()
        if not obj:
            raise ValueError("Not found")

        self.model = obj
        self._audit_snapshot = obj.json()

    def execute(self):
        super().execute()
        self.session.delete(self.model)
        self.modeling_action = "delete"

