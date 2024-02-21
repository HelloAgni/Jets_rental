from fastapi import APIRouter, Depends, HTTPException

from app.core.user import auth_backend, fastapi_users, only_verify_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)


@router.delete(
        '/users/{id}',
        tags=['Users'],
        deprecated=True
)
def delete_user(id: str):
    """
    No one can delete users.\n
    Just use deactivate.\n
    Block method or raise exception!
    """
    raise HTTPException(
        status_code=405,
        detail='Just use deactivate!!!'
    )


@router.get(
        "/who-iam",
        tags=['Check_verify'],
)
async def authenticated_route(user: User = Depends(only_verify_user)):
    """
    Checking if user is verified.
    """
    if user:
        return {"message": f"Hello {user.email}, "
                           f"verified: {user.is_verified}!"}
    return {'hello': 'We dont know you! Register or sign in and verify!'}
