from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Category, TodoItem, User


class TodoItemDTO(SQLAlchemyDTO[TodoItem]):
    pass


class TodoItemCreateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "done", "assigned_to", "categories.0.name"}
    )


class TodoItemUpdateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id", "assigned_to", "categories.0.name"}, partial=True)


class UserDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"items"})


class UserFullDTO(SQLAlchemyDTO[User]):
    pass


class UserCreateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"})


class UserUpdateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"}, partial=True)


class CategoryDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"items"})


class CategoryFullDTO(SQLAlchemyDTO[Category]):
    pass


class CategoryCreateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"})


class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"}, partial=True)
