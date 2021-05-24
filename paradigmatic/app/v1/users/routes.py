import logging
import typing as t

from paradigmatic.app.v1.core.auth import get_current_active_superuser, get_current_active_user
from fastapi import APIRouter, Depends, File, Request, Response, UploadFile, Form, HTTPException

from . import schemas
from .controller import (create_user, delete_user, edit_user, get_user, get_user_self_details,get_users)

users_router = r = APIRouter()


@r.get(
    "/users",
    response_model=t.List[schemas.User],
)
async def users_list(
        response: Response,
        current_user=Depends(get_current_active_superuser),
):
    """
    Get all Users
    """
    users = get_users()
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


@r.post("/users", response_model=schemas.User)
async def user_create(
        request: Request,
        user: schemas.UserCreate,
        current_user=Depends(get_current_active_superuser)
):
    """
    Create a new User
    """
    return create_user(user).to_mongo().to_dict()


@r.get("/users/me", response_model=schemas.UserSelfDetailed, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_active_user)):
    """
    Get own User
    """
    return get_user_self_details(current_user)


@r.get("/users/{user_id}", response_model=schemas.User)
async def user_details(
        request: Request,
        user_id: str,
        current_user=Depends(get_current_active_superuser),
):
    """
    Get any User details
    """
    user = get_user(user_id)
    return user.to_mongo().to_dict()


@r.put("/users/{user_id}", response_model=schemas.User)
async def user_edit(
        request: Request,
        user_id: str,
        user: schemas.UserEdit,
        current_user=Depends(get_current_active_user),
):
    """
    Update existing User
    """
    if str(user_id) != str(current_user.id):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    updated_user = edit_user(user_id, user)
    return updated_user.to_mongo().to_dict()


@r.delete(
    "/users/{user_id}", response_model=schemas.User, response_model_exclude_none=True
)
async def user_delete(
        request: Request,
        user_id: str,
        current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing User
    """
    resp = delete_user(user_id)
    if resp is True:
        return {"success": True}
    return {"success": False}
