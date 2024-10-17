from litestar import Litestar

from app.controllers import (
    AuthController,
    CategoryController,
    CommentController,
    ItemController,
    UserController,
)
from app.database import sqlalchemy_plugin
from app.security import oauth2_auth

app = Litestar(
    route_handlers=[
        AuthController,
        CategoryController,
        CommentController,
        ItemController,
        UserController,
    ],
    plugins=[sqlalchemy_plugin],
    debug=True,
    on_app_init=[oauth2_auth.on_app_init],
)
