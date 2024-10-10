from litestar import Litestar

from app.controllers import CategoryController, ItemController, UserController
from app.database import sqlalchemy_plugin

app = Litestar(
    route_handlers=[ItemController, UserController, CategoryController],
    plugins=[sqlalchemy_plugin],
    debug=True,
)
