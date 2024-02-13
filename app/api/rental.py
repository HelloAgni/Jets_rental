from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_jet_exists, check_rental_before_edit,
                                check_rental_intersections)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.rental import rental_crud
from app.models import Jet, Rental, User
from app.schemas.rental import R1, R2, R3, RentalCreate, RentalDB, RentalUpdate

router = APIRouter()


@router.post(
    '/',
    response_model=RentalDB
)
async def create_rental(
    rental: RentalCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Create rental object.
    """
    await check_jet_exists(
        rental.jet_id, session
    )
    await check_rental_intersections(
        **rental.dict(), session=session
    )
    new_rental = await rental_crud.create(
        rental, session, user
    )
    return new_rental


@router.get(
    '/',
    response_model=list[RentalDB],
    dependencies=[Depends(current_superuser)],
    #
    response_model_exclude_none=True,
)
async def get_all_rentals(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all Rental objects.\n
    Only available to super users.
    """
    rentals = await rental_crud.get_multi(session)
    print(rentals)
    return rentals


@router.get(
        '/my_reservations',
        response_model=list[RentalDB],
        response_model_exclude={'user_id'},  # Optional
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Get all Rental objects by current user.\n
    Only available to current user.
    """
    result = await rental_crud.get_by_user(
        session=session, user=user
        )
    return result


@router.delete(
    '/{rental_id}',
    response_model=RentalDB
)
async def delete_rental(
    rental_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Rental delete object.\n
    Only available to current user and super user.
    """
    rental = await check_rental_before_edit(
        rental_id,
        session,
        user
    )
    rental = await rental_crud.remove(
        rental, session
    )
    return rental


@router.patch(
    '/{rental_id}',
    response_model=RentalDB,
)
async def update_rental(
    rental_id: int,
    obj_in: RentalUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Rental update object.
    Only available to current user and super user.
    """
    rental = await check_rental_before_edit(
        rental_id,
        session,
        user
    )
    await check_rental_intersections(
        **obj_in.model_dump(),
        rental_id=rental_id,
        jet_id=rental.jet_id,
        session=session
    )
    rental = await rental_crud.update(
        db_obj=rental,
        # На обновление передаем объект класса Rental.
        obj_in=obj_in,
        session=session
    )
    return rental


@router.get(
        '/rental-user-info',
        response_model=list[R3],
        response_model_exclude_none=True
)
async def rental_user_info(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Check all rentals by current user.
    """
    duration = (func.date_part('day', Rental.end_date) -
                func.date_part('day', Rental.start_date))
    total_price = duration * Jet.price
    result = await session.execute(select(
        Rental.id.label('rental_id'),
        Rental.jet_id,
        Rental.start_date,
        Rental.end_date,
        Rental.user_id,
        User.email.label('user_email'),  # type: ignore
        Jet.name.label('jet_name'),
        Jet.price,
        duration.label('duration'),
        total_price.label('total_price')
        ).join(Jet, Rental.jet_id == Jet.id
               ).where(Rental.user_id == user.id
                       ).join(User, Rental.user_id == User.id))  # type: ignore
    return [elem._asdict() for elem in result]


@router.get(
        '/rental-info-1',
        response_model=list[R1],
        response_model_exclude_none=True
)
async def rental_info_v1(
    session: AsyncSession = Depends(get_async_session)

):
    """
    Rental days duration v1.
    Available for all users.
    """
    duration = (func.date_part('day', Rental.end_date) -
                func.date_part('day', Rental.start_date))
    total_price = duration * Jet.price
    result = await session.execute(select(
        Rental.id.label('rental_id'),
        Rental.jet_id,
        Rental.start_date,
        Rental.end_date,
        Jet.name.label('jet_name'),
        Jet.price,
        duration.label('duration'),
        total_price.label('total_price')
        ).join(Jet, Rental.jet_id == Jet.id))
    return [elem._asdict() for elem in result]


@router.get(
        '/rental-info-2',
        response_model=list[R2],
        response_model_exclude_none=True
)
async def rental_info_v2(
    session: AsyncSession = Depends(get_async_session)

):
    """
    Rental days duration v2.
    Available for all users.
    """
    duration = (func.date_part('day', Rental.end_date) -
                func.date_part('day', Rental.start_date))
    total_price = duration * Jet.price
    q = await session.execute(select(
        Rental,
        Jet.name,
        Jet.price,
        duration.label('duration'),
        total_price.label('total_price')
        ).join(Jet, Rental.jet_id == Jet.id))
    new = [a._asdict() for a in q]
    return new
