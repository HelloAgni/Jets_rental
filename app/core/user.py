"""
Настройки библиотеки FastAPI Users
"""
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate
from .token_activate import fake_email_send


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    asynchronous generator get_user_db.
    It provides database access via SQLAlchemy
    and will be used as a dependency / Depends in the future
    for an object of the UserManager class
    """
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    verification_token_secret = 'SECRET'

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],  # type: ignore
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(f'User: {user.email} has been registered.')

    # Check User by token
    # ../verify
    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has been verified")

    # Verify User by email - and get token
    # ../request_verify_token
    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        fake_email_send(
            user_id=user.id,
            user_email=user.email,
            user_first_name=user.first_name,
            user_last_name=user.last_name,
            token=token
            )
        print(
            f'Verification requested for user_id {user.id}. '
            f'Verification token: {token}'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',  # Custom backend name (must be unique)
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
any_user = fastapi_users.current_user(optional=True)
only_verify_user = fastapi_users.current_user(
    optional=True, active=True, verified=True)
