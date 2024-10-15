from litestar import Litestar

from app.controllers import (
    AuthController,
    CategoryController,
    ItemController,
    UserController,
)
from app.database import sqlalchemy_plugin
from app.security import oauth2_auth

app = Litestar(
    route_handlers=[ItemController, UserController, CategoryController, AuthController],
    plugins=[sqlalchemy_plugin],
    debug=True,
    on_app_init=[oauth2_auth.on_app_init]
)
