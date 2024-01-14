import contextlib
from datetime import date

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

# Превращаем асинхронные генераторы в асинхронные менеджеры контекста.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr,
        password: str,
        is_superuser: bool = True,
        is_verified: bool = True,
        *,
        first_name: str,
        last_name: str,
        birth_date: date,
        ):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            is_verified=is_verified,
                            first_name=first_name,
                            last_name=last_name,
                            birth_date=birth_date
                        )
                    )
                    # print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


# check .env file with super user params
async def create_first_superuser():
    if settings.super_email and settings.super_password:
        await create_user(
            email=settings.super_email,
            password=settings.super_password,
            first_name=settings.first_name,
            last_name=settings.last_name,
            birth_date=settings.birth_date
        )
    if settings.bot_email and settings.bot_password:
        await create_user(
            email=settings.bot_email,
            password=settings.bot_password,
            is_superuser=False,
            first_name=settings.bot_first_name,
            last_name=settings.bot_last_name,
            birth_date=settings.bot_birth_date
            )
