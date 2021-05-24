import typing as t

from paradigmatic.app.v1.core.security import get_password_hash
from fastapi import HTTPException, status, UploadFile

from . import models as user_models, schemas


def get_user(user_id: str) -> user_models.User:
    user = user_models.User.objects.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(new_user: schemas.UserCreate) -> user_models.User:
    new_user_dict = new_user.dict(exclude_unset=True)
    if "password" in new_user_dict and new_user_dict["password"]:
        hashed_password = get_password_hash(new_user_dict["password"])
        new_user_dict["hashed_password"] = hashed_password
    new_user_dict.pop("password")
    new_user = user_models.User(**new_user_dict).save()
    return new_user


def get_users(skip: int = 0, limit: int = 100) -> t.List[schemas.User]:
    return [o.to_mongo().to_dict() for o in user_models.User.objects()[skip:limit]]


def get_user_by_email(email: str) -> user_models.User:
    return user_models.User.objects(email=email).first()


def edit_user(user_id: str, user: schemas.UserEdit) -> schemas.User:
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]
    user_models.User.objects.get(id=user_id).update(**update_data)
    return get_user(user_id)


def delete_user(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    user.delete()
    return True


def get_user_self_details(current_user: schemas.User) -> dict:
    current_user = current_user.to_mongo().to_dict()
    return current_user


def get_user_id_by_username(username=None):
    if username is not None:
        user_obj = user_models.User.objects.get(username=username)
        return user_obj.id
    all_user_objs = user_models.User.objects().all()
    user_id_by_username = {}
    for user in all_user_objs:
        user_id_by_username[user.username] = str(user.id)
    return user_id_by_username
