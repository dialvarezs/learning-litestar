from typing import Sequence
from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException

from app.dtos import (
    TodoItemCreateDTO,
    TodoItemDTO,
    TodoItemUpdateDTO,
    UserCreateDTO,
    UserDTO,
    UserFullDTO,
    UserUpdateDTO,
)
from app.models import TodoItem, User
from app.repositories import (
    TodoItemRepository,
    UserRepository,
    provide_todoitem_repo,
    provide_user_repo,
)


class ItemController(Controller):
    path = "/todo-items"
    tags = ["items"]
    dependencies = {"todoitem_repo": Provide(provide_todoitem_repo)}
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

    @post(
        "/",
        dto=TodoItemCreateDTO,
        dependencies={"user_repo": Provide(provide_user_repo)},
    )
    async def create_item(
        self,
        todoitem_repo: TodoItemRepository,
        user_repo: UserRepository,
        data: TodoItem,
    ) -> TodoItem:
        try:
            user_repo.get(data.assigned_to_id)
            return todoitem_repo.add(data)
        except NotFoundError:
            raise NotFoundException(
                detail=f"Usuario con id={data.assigned_to_id} no encontrado"
            )

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


class UserController(Controller):
    path = "/users"
    tags = ["users"]
    dependencies = {"user_repo": Provide(provide_user_repo)}
    return_dto = UserDTO

    @get("/")
    async def list_users(self, user_repo: UserRepository) -> Sequence[User]:
        return user_repo.list()

    @get("/{user_id:int}", return_dto=UserFullDTO)
    async def get_user(self, user_repo: UserRepository, user_id: int) -> User:
        try:
            return user_repo.get(user_id)
        except NotFoundError:
            raise NotFoundException(detail=f"Usuario con id={user_id} no encontrado")

    @post("/", dto=UserCreateDTO)
    async def create_user(self, user_repo: UserRepository, data: User) -> User:
        return user_repo.add(data)

    @patch("/{user_id:int}", dto=UserUpdateDTO)
    async def patch_user(
        self, user_repo: UserRepository, user_id: int, data: DTOData[User]
    ) -> User:
        try:
            user, _ = user_repo.get_and_update(
                id=user_id, **data.as_builtins(), match_fields=["id"]
            )
            return user
        except NotFoundError:
            raise NotFoundException(detail=f"Usuario con id={user_id} no encontrado")

    @delete("/{user_id:int}")
    async def delete_user(self, user_repo: UserRepository, user_id: int) -> None:
        try:
            user_repo.delete(user_id)
        except NotFoundError:
            raise NotFoundException(detail=f"Usuario con id={user_id} no encontrado")
