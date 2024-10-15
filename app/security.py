from typing import Any
from advanced_alchemy.exceptions import NotFoundError
from litestar.connection import ASGIConnection
from litestar.contrib.jwt import OAuth2PasswordBearerAuth, Token
from litestar.exceptions import NotFoundException
from pwdlib import PasswordHash

from app.models import User
from app.database import db_config
from app import repositories
token_secret = "serversecret"

password_hasher = PasswordHash.recommended()


def retrieve_user_handler(
    token: "Token", _: "ASGIConnection[Any, Any, Any, Any]"
) -> User:
    Session = db_config.create_session_maker()
    try:
        with Session() as session:
            user_repo = repositories.UserRepository(session=session)
            return user_repo.get_one(username=token.sub)
    except NotFoundError:
        raise NotFoundException("User not found")


oauth2_auth = OAuth2PasswordBearerAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=token_secret,
    token_url="/auth/login",
    exclude=["/auth/login", "/schema"],
)
