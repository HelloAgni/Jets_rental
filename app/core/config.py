from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    app_title: str = 'Empty title'
    description: str = 'Empty description'

    # Postgres
    database_url: str = 'postgresql+asyncpg://fapi:fapix@localhost:5432/fapi_loc_db'

    # Docker compose
    # database_url: str = 'postgresql+asyncpg://fapi:fapix@db:5432/fapi_db'

    # SQLite
    # database_url: str = DATABASE_URL=sqlite+aiosqlite:///./fastapijetz.db
    secret: str = "SECRET"  # for User token

    # .env
    super_email: EmailStr | None = None
    super_password: str | None = None
    first_name: str = 'Super'
    last_name: str = 'Admin'
    birth_date: str = '1999-01-19'

    # bot user
    bot_email: EmailStr | None = None
    bot_password: str | None = None
    bot_first_name: str = 'Mano'
    bot_last_name: str = 'Boto'
    bot_birth_date: str = '2000-01-01'

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


settings = Settings()  # type: ignore
# print('Settings ENV:', settings.model_dump())
# {'app_title': 'Jets Rental'...}
