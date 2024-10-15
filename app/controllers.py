from typing import Annotated, Sequence
from advanced_alchemy.exceptions import NotFoundError
from advanced_alchemy.filters import CollectionFilter
from litestar import Controller, Response, delete, get, patch, post
from litestar.contrib.jwt import OAuth2Login
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK

from app.dtos import (
    CategoryCreateDTO,
    CategoryDTO,
    CategoryFullDTO,
    CategoryUpdateDTO,
    TodoItemCreateDTO,
    TodoItemDTO,
    TodoItemUpdateDTO,
    UserCreateDTO,
    UserDTO,
    UserFullDTO,
    UserLoginDTO,
    UserUpdateDTO,
)
from app.models import Category, TodoItem, User
from app.repositories import (
    CategoryRepository,
    TodoItemRepository,
    UserRepository,
    provide_category_repo,
    provide_todoitem_repo,
    provide_user_repo,
)
from app.security import password_hasher, oauth2_auth


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
        dependencies={
            "user_repo": Provide(provide_user_repo),
            "category_repo": Provide(provide_category_repo),
        },
    )
    async def create_item(
        self,
        todoitem_repo: TodoItemRepository,
        user_repo: UserRepository,
        category_repo: CategoryRepository,
        data: TodoItem,
    ) -> TodoItem:
        try:
            # verifica si usuario existe
            user_repo.get(data.assigned_to_id)
            # verifica categorías
            data.categories = category_repo.list(
                CollectionFilter(field_name="id", values=[c.id for c in data.categories])
            )

            return todoitem_repo.add(data)
        except NotFoundError:
            raise NotFoundException(
                detail=f"Usuario con id={data.assigned_to_id} no encontrado"
            )

    @patch(
        "/{item_id:int}",
        dto=TodoItemUpdateDTO,
        dependencies={
            "category_repo": Provide(provide_category_repo),
        },
    )
    async def patch_item(
        self,
        todoitem_repo: TodoItemRepository,
        category_repo: CategoryRepository,
        item_id: int,
        data: DTOData[TodoItem],
    ) -> TodoItem:
        try:
            data_dict = data.as_builtins()
            if "categories" in data_dict:
                data_dict["categories"] = category_repo.list(
                    CollectionFilter(
                        field_name="id", values=[c.id for c in data_dict["categories"]]
                    )
                )

            item, _ = todoitem_repo.get_and_update(
                id=item_id, **data_dict, match_fields=["id"]
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
        return user_repo.add_hashed(data)

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


class CategoryController(Controller):
    path = "/categories"
    tags = ["categories"]
    dependencies = {"category_repo": Provide(provide_category_repo)}
    return_dto = CategoryDTO

    @get("/")
    async def list_categories(
        self, category_repo: CategoryRepository
    ) -> Sequence[Category]:
        return category_repo.list()

    @get("/{category_id:int}", return_dto=CategoryFullDTO)
    async def get_category(
        self, category_repo: CategoryRepository, category_id: int
    ) -> Category:
        try:
            return category_repo.get(category_id)
        except NotFoundError:
            raise NotFoundException(
                detail=f"Categoría con id={category_id} no encontrada"
            )

    @post("/", dto=CategoryCreateDTO)
    async def create_category(
        self, category_repo: CategoryRepository, data: Category
    ) -> Category:
        return category_repo.add(data)

    @patch("/{category_id:int}", dto=CategoryUpdateDTO)
    async def patch_category(
        self,
        category_repo: CategoryRepository,
        category_id: int,
        data: DTOData[Category],
    ) -> Category:
        try:
            category, _ = category_repo.get_and_update(
                id=category_id, **data.as_builtins(), match_fields=["id"]
            )
            return category
        except NotFoundError:
            raise NotFoundException(
                detail=f"Categoría con id={category_id} no encontrada"
            )

    @delete("/{category_id:int}")
    async def delete_category(
        self, category_repo: CategoryRepository, category_id: int
    ) -> None:
        try:
            category_repo.delete(category_id)
        except NotFoundError:
            raise NotFoundException(
                detail=f"Categoría con id={category_id} no encontrada"
            )


class AuthController(Controller):
    path = "/auth"
    tags = ["auth"]

    @post(
        "/login",
        dto=UserLoginDTO,
        dependencies={"user_repo": Provide(provide_user_repo)},
    )
    async def login(
        self,
        data: Annotated[User, Body(media_type=RequestEncodingType.URL_ENCODED)],
        user_repo: UserRepository,
    ) -> "Response[OAuth2Login]":
        user = user_repo.get_one_or_none(username=data.username)

        if user is not None and password_hasher.verify(data.password, user.password):
            return oauth2_auth.login(
                identifier=str(user.username), token_extras={"name": user.fullname}
            )
        else:
            raise HTTPException(
                status_code=401, detail="Usuario o contraseña incorrecta"
            )

    @post("/logout")
    async def logout(self) -> Response[None]:
        response = Response(content=None, status_code=HTTP_200_OK)
        response.delete_cookie("token")

        return response
