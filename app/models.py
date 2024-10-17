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
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

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
        back_populates="items",
        secondary="items_categories",
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="item")

    def __repr__(self) -> str:
        return f"<TodoItem(id={self.id},title={self.title},done={self.done})>"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    items: Mapped[list["TodoItem"]] = relationship(
        back_populates="categories",
        secondary="items_categories",
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id},name={self.name})>"


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(32))
    item_id: Mapped[int] = mapped_column(ForeignKey("todoitems.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    item: Mapped["TodoItem"] = relationship("TodoItem", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments")


class ItemCategory(Base):
    __tablename__ = "items_categories"

    item_id: Mapped[int] = mapped_column(ForeignKey("todoitems.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        primary_key=True,
    )
