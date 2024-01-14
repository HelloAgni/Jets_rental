from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Rental(Base):
    """
    Rental Model.
    """
    start_date: Mapped[date]
    end_date: Mapped[date]
    jet_id: Mapped[int] = mapped_column(
        ForeignKey('jet.id')  # if added naming_convention
        # else:
        # ForeignKey('jet.id', name='fk_rental_jet_id_jet')
        # FK_name -> cur. table -> cur. column -> other table
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id')
    )

    def __init__(
            self, start_date: date,
            end_date: date,
            jet_id: int,
            user_id: int
            ):
        self.start_date = start_date
        self.end_date = end_date
        self.jet_id = jet_id
        self.user_id = user_id

    @hybrid_property
    def duration(self):
        return (self.end_date - self.start_date).days

    __table_args__ = (
        CheckConstraint('start_date < end_date',),
    )

    def __repr__(self) -> str:
        return (
            f'Start: {self.start_date} '
            f'End: {self.end_date}'
            )
