from sqlmodel import select
from core.base_service import BaseService

class BaseQueryService(BaseService):
    model_class = None  # must be set by orchestrator

    def execute(self):
        q = self.input_data
        Model = self.model_class

        statement = select(Model)

        if q.id is not None:
            statement = statement.where(Model.id == q.id)

        if q.name is not None:
            statement = statement.where(Model.name == q.name)

        if q.like is not None:
            pattern = f"%{q.like}%"
            statement = statement.where(Model.name.like(pattern))

        column = getattr(Model, "name", None)
        if column is not None:
            statement = statement.order_by(column)

        self.model = self.session.exec(statement).all()
