# crud.py
from sqlmodel import SQLModel, Session, select
from typing import List, Optional, TypeVar
import models

# 定义一个泛型类型，代表我们的模型类
ModelType = TypeVar("ModelType", bound=SQLModel)

def create_item(session: Session, model_class: type[ModelType], item_data: SQLModel):
    """通用创建函数"""
    db_item = model_class.model_validate(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_item(session: Session, model_class: type[ModelType], item_id: int):
    """通用根据ID获取单个对象函数"""
    return session.get(model_class, item_id)

def get_items(session: Session, model_class: type[ModelType], offset: int = 0, limit: int = 100):
    """通用获取对象列表函数"""
    statement = select(model_class).offset(offset).limit(limit)
    results = session.exec(statement).all()
    return results

def get_item_by_field(session: Session, model_class: type[ModelType], field_name: str, field_value: str):
    """通用根据某个字段的值获取单个对象（用于检查唯一性）"""
    statement = select(model_class).where(getattr(model_class, field_name) == field_value)
    return session.exec(statement).first()

def update_item(session: Session, model_class: type[ModelType], item_id: int, item_data: SQLModel):
    """通用更新函数"""
    db_item = session.get(model_class, item_id)
    if not db_item:
        return None
    item_updates = item_data.model_dump(exclude_unset=True)
    for key, value in item_updates.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def delete_item(session: Session, model_class: type[ModelType], item_id: int):
    """通用删除函数"""
    db_item = session.get(model_class, item_id)
    if not db_item:
        return None
    session.delete(db_item)
    session.commit()
    return {"ok": True}