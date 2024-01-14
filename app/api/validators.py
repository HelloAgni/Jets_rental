from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.rental import rental_crud
from app.crud.jet import jet_crud
from app.models import Jet, Rental, User


async def check_rental_before_edit(
        rental_id: int,
        session: AsyncSession,
        user: User,
) -> Rental:
    """Check if rental object exists."""
    rental = await rental_crud.get(
        obj_id=rental_id, session=session
    )
    if not rental:
        raise HTTPException(
            status_code=404,
            detail='Rental not found (validators)'
        )
    if rental.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='You cannot edit or delete others rental (validators)'
        )
    return rental


async def check_rental_intersections(**kwargs) -> None:
    """
    Check rental intersections, if exists raise error.
    """
    rentals = await rental_crud.get_rental_at_the_same_time(
        **kwargs
    )
    if rentals:
        raise HTTPException(
            status_code=422,
            detail=f'Intersection for jet_id: '
                   f'{kwargs["jet_id"]} {str(*rentals)}'
        )


async def check_jet_exists(
    jet_id: int,
    session: AsyncSession
) -> Jet:
    """Check Jet obj by id exists."""
    jet = await jet_crud.get(jet_id, session)
    if jet is None:
        raise HTTPException(
            status_code=404,
            detail=f'Jet id: {jet_id} not found!'
        )
    return jet


async def check_name_duplicate(
    jet_name: str,
    session: AsyncSession,
) -> None:
    """Check jet obj by name exists."""

    jet_id = await jet_crud.get_jet_id_by_name(
        jet_name,
        session
        )
    if jet_id is not None:
        raise HTTPException(
            status_code=422,
            detail=f'Jet name: {jet_name} exists!',
        )
