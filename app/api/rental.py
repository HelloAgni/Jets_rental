from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_rental_before_edit,
                                check_rental_intersections,
                                check_jet_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.rental import rental_crud
from app.models import User
from app.schemas.rental import RentalCreate, RentalDB, RentalUpdate

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
)
async def get_all_rentals(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all Rental objects.\n
    Only available to super users.
    """
    rentals = await rental_crud.get_multi(session)
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
        # id обновляемого объекта бронирования,
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
