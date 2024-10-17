from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import Category, Comment, TodoItem, User


class TodoItemDTO(SQLAlchemyDTO[TodoItem]):
    pass


class TodoItemCreateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "done", "assigned_to", "comments", "categories.0.name"},
    )


class TodoItemUpdateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "assigned_to", "comments", "categories.0.name"},
        partial=True,
    )


class UserDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"items", "password", "comments"})


class UserFullDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password", "comments"})


class UserCreateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items", "comments"})


class UserUpdateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items", "comments"}, partial=True)


class UserLoginDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(include={"username", "password"})


class CategoryDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"items"})


class CategoryFullDTO(SQLAlchemyDTO[Category]):
    pass


class CategoryCreateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"})


class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(exclude={"id", "items"}, partial=True)


class CommentDTO(SQLAlchemyDTO[Comment]):
    pass


class CommentCreateDTO(SQLAlchemyDTO[Comment]):
    config = SQLAlchemyDTOConfig(exclude={"id", "user", "todo_item"})


class CommentUpdateDTO(SQLAlchemyDTO[Comment]):
    config = SQLAlchemyDTOConfig(exclude={"id", "user", "todo_item"}, partial=True)
