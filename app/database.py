from dataclasses import dataclass
from typing import Optional

from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig

from app.models import Base

db_config = SQLAlchemySyncConfig(
    connection_string="sqlite:///todo.sqlite3", metadata=Base.metadata, create_all=True
)

sqlalchemy_plugin = SQLAlchemyPlugin(db_config)


@dataclass
class TodoItem:
    title: str
    done: bool


@dataclass
class TodoItemUpdate:
    title: Optional[str] = None
    done: Optional[bool] = None


TODO_LIST: list[TodoItem] = [
    TodoItem(title="Aprender Python", done=True),
    TodoItem(title="Aprender SQLAlchemy", done=True),
    TodoItem(title="Aprender Litestar", done=False),
]
