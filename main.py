from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import Annotated

from database import engine, get_session, create_db_and_tables
from models import WorkOrder
from schemas import WorkOrderCreate, WorkOrderRead

# 创建表 (应用启动时)
create_db_and_tables()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/workorders/", response_model=WorkOrderRead, status_code=201)
def create_work_order(work_order: WorkOrderCreate, session: Annotated[Session, Depends(get_session)]):
    db_work_order = WorkOrder.from_orm(work_order)
    session.add(db_work_order)
    session.commit()
    session.refresh(db_work_order)
    return db_work_order

@app.get("/workorders/", response_model=list[WorkOrderRead])
def read_work_orders(session: Annotated[Session, Depends(get_session)]):
    work_orders = session.exec(select(WorkOrder)).all()
    return work_orders