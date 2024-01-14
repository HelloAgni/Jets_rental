from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from app.crud.base import CRUDBase
# from app.models.rental import Rental
from app.models import Rental, User


class CRUDRental(CRUDBase):

    async def get_rental_at_the_same_time(
            self,
            *,
            jet_id: int,
            start_date: date,
            end_date: date,
            rental_id: int | None = None,
            session: AsyncSession
    ) -> Sequence[Rental]:
        """
        Found any rental at the same time.
        """
        select_stmt = select(Rental).where(
            Rental.jet_id == jet_id,
            and_(
                start_date <= Rental.end_date,
                end_date >= Rental.start_date
            )
        )
        if rental_id:
            select_stmt = select_stmt.where(
                Rental.id != rental_id
            )
        rentals = await session.execute(select_stmt)
        # rentals = rentals.scalars().all()
        return rentals.scalars().all()

    async def get_rental_for_jet(
            self,
            jet_id: int,
            session: AsyncSession
    ):
        """
        Found all rentals for jet_id.
        """
        rentals = await session.execute(
            select(Rental).where(
                Rental.jet_id == jet_id,
                # Rental.end_date > date.today()  # Optional
            )
        )
        # rentals = rentals.scalars().all()
        return rentals.scalars().all()

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ):
        """
        Get list of reservation object by current user.
        """
        rentals = await session.execute(
            select(Rental).where(
                Rental.user_id == user.id
            )
        )
        return rentals.scalars().all()


rental_crud = CRUDRental(Rental)
