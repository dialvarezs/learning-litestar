
from litestar import Controller, delete, get, patch, post, put

from app.database import TODO_LIST, TodoItem, TodoItemUpdate


class ItemController(Controller):
    path = "/todo-items"

    @get("/")
    async def list_items(self, done: bool | None = None) -> list[TodoItem]:
        if done is None:
            return TODO_LIST
        return [x for x in TODO_LIST if x.done == done]

    @get("/{item_id:int}")
    async def get_item(self, item_id: int) -> TodoItem:
        return TODO_LIST[item_id - 1]

    @post("/")
    async def create_item(self, data: TodoItem) -> TodoItem:
        TODO_LIST.append(data)
        return data

    @put("/{item_id:int}")
    async def update_item(self, item_id: int, data: TodoItem) -> TodoItem:
        TODO_LIST[item_id - 1] = data
        return data

    @patch("/{item_id:int}")
    async def patch_item(self, item_id: int, data: TodoItemUpdate) -> TodoItem:
        for k, v in data.__dict__.items():
            setattr(TODO_LIST[item_id - 1], k, v)
        return TODO_LIST[item_id - 1]

    @delete("/{item_id:int}")
    async def delete_item(self, item_id: int) -> None:
        del TODO_LIST[item_id - 1]