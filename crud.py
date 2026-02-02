# crud.py
from sqlmodel import SQLModel, Session, select
from typing import List, Optional, Type, TypeVar
import model

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

def update_item_with_change_count(
    session: Session, 
    model_class: Type[ModelType], 
    item_id: int, 
    item_data: SQLModel, # 这个 item_data 现在应该包含 change_count
    change_count_field: str = "change_count" # 版本字段的名称，默认为 'change_count'
) -> ModelType | None:
    """
    支持乐观锁的更新函数。
    """
    # 1. 从 item_data 中提取 change_count 值，并从要更新的数据中移除它
    #    因为 change_count 是用来做 WHERE 条件的，不是要 SET 的字段
    item_updates_dict = item_data.model_dump(exclude_unset=True)
    client_change_count = item_updates_dict.pop(change_count_field, None)

    if client_change_count is None:
        # 如果客户端没有提供 change_count，则无法执行乐观锁更新
        # 可以选择抛出异常或直接走普通更新逻辑
        # 这里我们选择抛出错误，强制使用乐观锁
        raise ValueError(f"The '{change_count_field}' field is required for updating.")

    # 2. 根据 ID 和 change_count 构建查询和更新语句
    #    这是原子操作的关键
    db_item = session.get(model_class, item_id)
    if not db_item:
        return None # 没找到对象

    # 检查版本是否匹配
    current_db_change_count = getattr(db_item, change_count_field)
    if current_db_change_count != client_change_count:
        # 版本不匹配，说明数据已被修改
        return None # 返回 None 表示冲突

    # 3. 版本匹配，执行更新
    for key, value in item_updates_dict.items():
        setattr(db_item, key, value)
        
    # 4. 递增版本号
    new_change_count = client_change_count + 1
    setattr(db_item, change_count_field, new_change_count)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item