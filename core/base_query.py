from sqlmodel import SQLModel

class BaseQuery(SQLModel):
    id: int | None = None
    name: str | None = None
    like: str | None = None
