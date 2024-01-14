from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_jet_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.rental import rental_crud
from app.crud.jet import jet_crud
from app.models.jet import Jet
from app.schemas.rental import RentalDB
from app.schemas.jet import JetCreate, JetDB, JetUpdate

router = APIRouter()


@router.get(
        '/{jet_id}',
        response_model=JetDB,
        response_model_exclude_none=True
)
async def get_single(
    jet_id: int = Path(example=1, ge=1),
    session: AsyncSession = Depends(get_async_session)
):
    """Get single."""
    await check_jet_exists(jet_id, session)
    jet = await jet_crud.get(jet_id, session)
    return jet


@router.get(
        '/',
        response_model=list[JetDB],
        response_model_exclude_none=True
)
async def get_all_jets(
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(ge=0, example=0),
    page_size: int = Query(ge=1, le=20, example=20)
):
    """
    Get all Jets objects.
    With pagination.
    """
    jets = await jet_crud.get_multi(session)
    return jets[skip: page_size]


@router.post(
        '/',
        response_model=JetDB,
        response_model_exclude_none=True,
        dependencies=[Depends(current_superuser)],  # check user status
)
async def create_new_jet(
        jet: JetCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Create Jet object.\n
    Only available to super users.
    """

    await check_name_duplicate(jet.name, session)

    new_jet = await jet_crud.create(jet, session)
    return new_jet


@router.patch(
    '/{jet_id}',
    response_model=JetDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_jet(
    jet_id: int,
    obj_in: JetUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Patch Jet object.
    Only available to super users.
    """
    jet = await check_jet_exists(
        jet_id,
        session
        )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    jet = await jet_crud.update(
        jet,
        obj_in,
        session
    )
    return jet


@router.delete(
    '/{jet_id}',
    response_model=JetDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_jet(
    jet_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Jet:
    """
    Delete Jet object.
    Only available to super users.
    """
    jet = await check_jet_exists(jet_id, session)
    jet = await jet_crud.remove(jet, session)
    return jet


@router.get(
    '/{jet_id}/rentals',
    response_model=list[RentalDB],
    response_model_exclude={'user_id'},
)
async def get_rentals_for_jet(
    jet_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all rentals by jet id.
    """
    await check_jet_exists(jet_id, session)
    rentals = await rental_crud.get_rental_for_jet(
        jet_id=jet_id,
        session=session
    )
    return rentals


@router.get(
    '/by_attr/',
    response_model=list[JetDB]
)
async def get_by_my_attr(
    attr_name: str,
    value: int | str,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Filter objects by attribute name and value. \n
    attr_name: id, value: 2.
    """
    result_by_attribute = await jet_crud.get_by_attribute(
        attr_name=attr_name, attr_value=value, session=session
    )
    return result_by_attribute
