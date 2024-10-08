
from litestar import Litestar

from app.controllers import ItemController
from app.database import sqlalchemy_plugin

app = Litestar([ItemController], plugins=[sqlalchemy_plugin], debug=True)