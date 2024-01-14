from fastapi import APIRouter, Depends, HTTPException

from app.core.user import (any_user, auth_backend, fastapi_users,
                           only_verify_user)
from app.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.delete(
        '/users/{id}',
        tags=['users'],
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

# # Refactor delete endpoint stage 1
# @router.delete(
#         '/users/{id}'
# )
# def block_method(id: int):
#     """
#     Raise exception for delete users endpoint
#     """
#     raise HTTPException(
#         status_code=405,
#         detail='Deleting users is prohibited!'
#     )


# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

# # @router.post(
# #     '/auth/verify',
# #     deprecated=True,
# #     tags=["auth"]
# # )
# # async def verify():
# #     pass

# @router.get(
#         "/who-iam",
#         tags=['My simple routers'],
# )
# # async def authenticated_route(user: User = Depends(any_user)):
# async def authenticated_route(user: User = Depends(only_verify_user)):
#     """
#     Checking if user is verified.
#     """
#     print('User API - 1', user)
#     if user:
#         return {"message": f"Hello {user.email}, verified: {user.is_verified}!"}
#     return {'hello': 'We dont know you! Register or sign in and verify!'}


# # Refactor delete endpoint stage 2
# @router.delete(
#         '/users/{id}',
#         tags=['users'],
#         deprecated=True
# )
# def deprecate_delete_user(id: int):
#     """
#     No one can delete users.\n
#     Just use deactivate.\n
#     Block method or raise exception!
#     """
#     pass
