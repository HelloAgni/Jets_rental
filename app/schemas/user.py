from datetime import date, timedelta

from fastapi_users import schemas
from pydantic import Field, validator


AGE_LIMIT = 18


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    birth_date: date


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(min_length=4, max_length=20, example='John')
    last_name: str = Field(min_length=4, max_length=20, example='Wick')
    birth_date: date = Field(default=date.today() - timedelta(days=30))

    @validator('first_name')
    def name_check(cls, value):
        if value == 'string':
            raise ValueError('Please, use name instead <string>')
        return value

    @validator('birth_date')
    def date_check(cls, value):
        if value >= date.today():
            raise ValueError('Please, set correct birth date')
        if value.year > date.today().year - AGE_LIMIT:
            raise ValueError(f'Sorry, only for {AGE_LIMIT} years old')
        return value


class UserUpdate(UserCreate, schemas.BaseUserUpdate):  # type: ignore
    pass
