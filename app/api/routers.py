"""Collect all endpoints."""
from fastapi import APIRouter
from .jet import router as jet_router
from .rental import router as rental_router
from .user import router as user_router

main_router = APIRouter()

main_router.include_router(
    jet_router,
    prefix='/jets',
    tags=['Jets.']
)
main_router.include_router(
    rental_router,
    prefix='/rental',
    tags=['Rental.']
)
main_router.include_router(
    user_router
)
