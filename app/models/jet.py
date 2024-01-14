from sqlalchemy import CheckConstraint, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app.core.db import Base

str25 = Annotated[str, mapped_column(String(25))]
str_text = Annotated[str,  mapped_column(Text, nullable=True)]


class Jet(Base):
    """
    Jet model.
    """
    name: Mapped[str25]
    jet_type: Mapped[str25]
    description: Mapped[str_text]
    speed: Mapped[int]
    flight_range: Mapped[int]
    passenger_capacity: Mapped[int]
    price: Mapped[int]
    rental = relationship('Rental', cascade='delete')

    __table_args__ = (
        # UniqueConstraint('name', 'type'),  # unique pair
        UniqueConstraint('name'),
        CheckConstraint('length(name) > 3',)
    )

    def __repr__(self) -> str:
        return f'ID: {self.id}, name: {self.name} type: {self.jet_type}'
