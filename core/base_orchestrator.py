from sqlmodel import Session
from core.database import engine

class BaseOrchestrator:
    def __init__(self, service_cls):
        self.service_cls = service_cls

    def run(self, data):
        with Session(engine) as session:
            try:
                service = self.service_cls(session)
                result = service.run(data)
                session.commit()
                return result
            except:
                session.rollback()
                raise
