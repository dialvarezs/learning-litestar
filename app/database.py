from advanced_alchemy.extensions.litestar import sync_autocommit_before_send_handler
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig

from app.models import Base

db_config = SQLAlchemySyncConfig(
    connection_string="sqlite:///todo.sqlite3",
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=sync_autocommit_before_send_handler,
)

sqlalchemy_plugin = SQLAlchemyPlugin(db_config)
