from litestar import Litestar

from app.controllers import ItemController, UserController
from app.database import sqlalchemy_plugin

app = Litestar(
    route_handlers=[ItemController, UserController],
    plugins=[sqlalchemy_plugin],
    debug=True,
)
