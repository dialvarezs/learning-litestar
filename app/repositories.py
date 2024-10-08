from typing import Sequence
from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TodoItem


class TodoItemRepository(SQLAlchemySyncRepository[TodoItem]):  # type: ignore
    model_type = TodoItem

    def list_filter_by_done(self, done: bool) -> Sequence[TodoItem]:
        return self.list(statement=select(TodoItem).where(TodoItem.done == done))


async def provide_todoitem_repo(db_session: Session) -> TodoItemRepository:
    return TodoItemRepository(session=db_session)
