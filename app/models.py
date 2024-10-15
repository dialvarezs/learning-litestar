from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    fullname: Mapped[str]
    password: Mapped[str]

    items: Mapped[list["TodoItem"]] = relationship(back_populates="assigned_to")

    def __repr__(self) -> str:
        return f"<User(id={self.id},username={self.username},fullname={self.fullname})>"


class TodoItem(Base):
    __tablename__ = "todoitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32))
    done: Mapped[bool] = mapped_column(default=False, server_default="0")
    assigned_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    assigned_to: Mapped["User"] = relationship(back_populates="items")
    categories: Mapped[list["Category"]] = relationship(
        back_populates="items", secondary="items_categories"
    )

    def __repr__(self) -> str:
        return f"<TodoItem(id={self.id},title={self.title},done={self.done})>"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    items: Mapped[list["TodoItem"]] = relationship(
        back_populates="categories", secondary="items_categories"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id},name={self.name})>"


class ItemCategory(Base):
    __tablename__ = "items_categories"

    item_id: Mapped[int] = mapped_column(ForeignKey("todoitems.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )
