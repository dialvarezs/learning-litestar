from typing import Sequence
from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, TodoItem, User
from app import security


class TodoItemRepository(SQLAlchemySyncRepository[TodoItem]):  # type: ignore
    model_type = TodoItem

    def list_filter_by_done(self, done: bool) -> Sequence[TodoItem]:
        return self.list(statement=select(TodoItem).where(TodoItem.done == done))


async def provide_todoitem_repo(db_session: Session) -> TodoItemRepository:
    return TodoItemRepository(session=db_session)


class UserRepository(SQLAlchemySyncRepository[User]):  # type: ignore
    model_type = User

    def add_hashed(self, data: User) -> User:
        data.password = security.password_hasher.hash(data.password)
        return self.add(data)



async def provide_user_repo(db_session: Session) -> UserRepository:
    return UserRepository(session=db_session)


class CategoryRepository(SQLAlchemySyncRepository[Category]):  # type: ignore
    model_type = Category


async def provide_category_repo(db_session: Session) -> CategoryRepository:
    return CategoryRepository(session=db_session)
