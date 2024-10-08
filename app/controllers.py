from typing import Sequence
from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException

from app.dtos import TodoItemCreateDTO, TodoItemDTO, TodoItemUpdateDTO
from app.models import TodoItem
from app.repositories import TodoItemRepository, provide_todoitem_repo


class ItemController(Controller):
    path = "/todo-items"
    dependencies = {"todoitem_repo": provide_todoitem_repo}
    return_dto = TodoItemDTO

    @get("/")
    async def list_items(
        self, todoitem_repo: TodoItemRepository, done: bool | None = None
    ) -> Sequence[TodoItem]:
        if done is None:
            return todoitem_repo.list()
        return todoitem_repo.list_filter_by_done(done)

    @get("/{item_id:int}")
    async def get_item(
        self, todoitem_repo: TodoItemRepository, item_id: int
    ) -> TodoItem:
        try:
            return todoitem_repo.get(item_id)
        except NotFoundError:
            raise NotFoundException(detail=f"Item con id={item_id} no encontrado")

    @post("/", dto=TodoItemCreateDTO)
    async def create_item(
        self, todoitem_repo: TodoItemRepository, data: TodoItem
    ) -> TodoItem:
        return todoitem_repo.add(data)

    @patch("/{item_id:int}", dto=TodoItemUpdateDTO)
    async def patch_item(
        self, todoitem_repo: TodoItemRepository, item_id: int, data: DTOData[TodoItem]
    ) -> TodoItem:
        try:
            item, _ = todoitem_repo.get_and_update(
                id=item_id, **data.as_builtins(), match_fields=["id"]
            )
            return item
        except NotFoundError:
            raise NotFoundException(detail=f"Item con id={item_id} no encontrado")

    @delete("/{item_id:int}")
    async def delete_item(self, todoitem_repo: TodoItemRepository, item_id: int) -> None:
        try:
            todoitem_repo.delete(item_id)
        except NotFoundError:
            raise NotFoundException(detail=f"Item con id={item_id} no encontrado")
