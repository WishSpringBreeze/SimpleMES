from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context



from sqlmodel import SQLModel
from model import *

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        compare_type=True,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # from database import engine
    # connectable = engine

    # 从 alembic.ini 获取配置，但我们会覆盖它
    configuration = config.get_section(config.config_ini_section)

    # 从环境变量或 alembic.ini 获取数据库 URL
    # 我们假设你的 DATABASE_URL 在 alembic.ini 里或者在环境变量里
    db_url = configuration.get('sqlalchemy.url') or os.getenv("DATABASE_URL")
    if not db_url:
         # 如果都找不到，抛出一个明确的错误
         raise ValueError("DATABASE_URL not configured in alembic.ini or environment variables.")

    # 创建引擎时，为 SQLite 添加 connect_args 来禁用事务
    connectable = engine_from_config(
        configuration, # 使用配置字典
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"check_same_thread": False} # 添加这个参数
    )

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
