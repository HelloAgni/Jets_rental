"""Collect all endpoints."""
from fastapi import APIRouter
from .user import router as user_router
from .rental import router as rental_router

main_router = APIRouter()

main_router.include_router(
    user_router
)
main_router.include_router(
    rental_router
)
