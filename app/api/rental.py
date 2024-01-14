from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from app.core.db import get_async_session
from app.models import Rental

from sqlalchemy import select
router = APIRouter()


@router.get(
    '/all-rentals-date'
)
async def rentals_date(
    session: AsyncSession = Depends(get_async_session)
):
    all_rentals = await session.execute(select(Rental))
    return all_rentals.scalars().all()


@router.get(
    '/duration-date'
)
async def durations_date(
    session: AsyncSession = Depends(get_async_session)
):
    all_rentals = await session.execute(select(
        # Rental.duration).where(Rental.id == 1))
        Rental.duration))
    return all_rentals.scalars().all()


@router.get(
    '/try-post-date'
)
async def try_post_date(
    session: AsyncSession = Depends(get_async_session),
    *,
    value_1: date = date.today(),
    value_2: date = date.today() + timedelta(days=2)
):
    """
    Try to add
    """
    obj = Rental(value_1, value_2)
    session.add(obj)
    await session.commit()
    return {'opop': obj, 'duration': obj.duration}
