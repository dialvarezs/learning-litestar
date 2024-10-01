from dataclasses import dataclass
from typing import Optional

from litestar import Controller, Litestar, delete, get, patch, post, put


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


app = Litestar([ItemController], debug=True)
