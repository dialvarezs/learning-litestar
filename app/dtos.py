from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models import TodoItem


class TodoItemDTO(SQLAlchemyDTO[TodoItem]):
    pass


class TodoItemCreateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id", "done"})

class TodoItemUpdateDTO(SQLAlchemyDTO[TodoItem]):
    config = SQLAlchemyDTOConfig(exclude={"id"}, partial=True)