from sqlmodel import Session
from core.database import engine

class BaseOrchestrator:
    def __init__(self, service_cls, read_schema=None):
        self.service_cls = service_cls
        self.read_schema = read_schema

    def run(self, data=None):
        with Session(engine) as session:
            try:
                service = self.service_cls(session)
                model = service.run(data)
                session.commit()

                # If no schema is provided, return True
                if not self.read_schema:
                    return True

                # If model is a list, convert each item
                if isinstance(model, list):
                    return [self.read_schema.from_orm(m) for m in model]

                # Otherwise convert a single model
                return self.read_schema.from_orm(model)

            except:
                session.rollback()
                raise
