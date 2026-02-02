from sqlmodel import Session
from history.modeling_audit_history import ModelingAuditHistory
import json
from base_service import BaseService

class BaseServiceModeling(BaseService):
    def save(self):
        super().save(self)
        if self.model:
            self.session.add(self.model)
            self.session.flush()
            self.session.refresh(self.model)

            history = ModelingAuditHistory(
                model_name=self.model.__class__.__name__,
                model_id=self.model.id,
                action="SAVE",
                data=json.dumps(self.model.dict())
            )
            self.session.add(history)

