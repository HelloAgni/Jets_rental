from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    app_title: str = 'Empty title'
    description: str = 'Empty description'
    database_url: str
    secret: str = "SECRET"  # for User token

    # .env
    super_email: EmailStr | None = None
    super_password: str | None = None
    first_name: str = 'Super'
    last_name: str = 'Admin'
    birth_date: str = '1999-01-19'

    # bot user
    bot_email: str = 'botman@mail.com'
    bot_password: str = 'bot123'
    bot_first_name: str = 'Mannn'
    bot_last_name: str = 'Bottt'
    bot_birth_date: str = '2000-01-01'

    class Config:
        env_file = '.env'


settings = Settings()  # type: ignore
# print(settings.model_dump())
# {'app_title': 'Jets Rental', 'description': 'Fictional service',
# 'database_url': 'sqlite+aiosqlite:///./fastapijetz.db'...}
