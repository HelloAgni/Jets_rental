from datetime import date

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Annotated

from app.core.db import Base

str20 = Annotated[str, mapped_column(String(20))]


# type: ignore  (fix for mypy)
class User(SQLAlchemyBaseUserTable[int], Base):  # type: ignore
    """
    User Model.
    """
    first_name: Mapped[str20]
    last_name: Mapped[str20]
    birth_date: Mapped[date]

    __table_args__ = (
        CheckConstraint(
            'length(first_name) > 3 and length(last_name) > 3',
            name='length_min4'),
    )

    def __repr__(self) -> str:
        return (
            f'User: {self.last_name} {self.first_name} '
            f'email: {self.email}'
        )
