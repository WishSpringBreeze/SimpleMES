from sqlmodel import Session
from history.modeling_audit_history import ModelingAuditHistory
import json

class BaseService:
    def __init__(self, session: Session):
        self.session = session
        self.model = None
        self.input_data = None

    def initialize(self, data):
        self.input_data = data

    def pre_validate(self):
        pass

    def validate(self):
        pass

    def execute(self):
        pass

    def post_execute(self):
        pass

    def save(self):
        pass

    def post_save(self):
        pass

    def run(self, data):
        self.initialize(data)
        self.pre_validate()
        self.validate()
        self.execute()
        self.post_execute()
        self.save()
        self.post_save()
        return self.model
