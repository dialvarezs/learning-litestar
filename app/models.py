from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todoitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    done: Mapped[bool] = mapped_column(default=False, server_default="0")

    def __repr__(self) -> str:
        return f"<TodoItem(id={self.id},title={self.title},done={self.done})>"
