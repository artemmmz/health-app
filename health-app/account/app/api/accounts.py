from typing import List

from fastapi import APIRouter, Query

from app.core.dependencies import AdminDep, DBAnnotation, UserAnnotation
from app.models.user_models import (
    UserModel,
    UserUpdate,
    UserCreationWithRoles,
    UserModelWithRoles,
    UserUpdateFull,
)
from app.services import UserService, RoleService

router = APIRouter()


@router.get('/me')
async def get_me(
    user: UserAnnotation, uow: DBAnnotation
) -> UserModelWithRoles:
    """Get the current user."""
    user_roles = await RoleService.get_roles(uow, user.id_)
    roles = []
    for role in user_roles:
        roles.append(role.role)
    user_model = UserModelWithRoles(**user.model_dump(), roles=roles)
    return user_model


@router.post('/update')
async def update_me(
    update_data: UserUpdate, user: UserAnnotation, uow: DBAnnotation
) -> UserModel:
    """Update the current user."""
    data = update_data.model_dump(exclude_none=True)
    result = await UserService.update_user(uow, user.id_, data)
    return result


@router.get('/', dependencies=[AdminDep])
async def get_all_users(
    uow: DBAnnotation,
    from_: int = Query(default=0, title='from', ge=0),
    count: int = Query(default=100, ge=0, le=100),
) -> List[UserModelWithRoles]:
    """Get all users."""
    users = await UserService.get_all_users(uow, from_, count)
    result = []
    for user in users:
        user_roles = await RoleService.get_roles(uow, user.id_)
        roles = [role.role for role in user_roles]
        user_model = UserModelWithRoles(**user.model_dump(), roles=roles)
        result.append(user_model)
    return result


@router.post('/', dependencies=[AdminDep])
async def create_user(
    data: UserCreationWithRoles, uow: DBAnnotation
) -> UserModelWithRoles:
    """Create a new user."""
    dict_data = data.model_dump(exclude={'roles'})
    dict_data['password'] = dict_data['password'].get_secret_value()
    user = await UserService.add_user(uow, dict_data)
    user_roles = []
    for role in data.roles:
        new_role = await RoleService.add_role(uow, user, role)
        user_roles.append(new_role)
    result = UserModelWithRoles(**user.model_dump(), roles=data.roles)
    return result


@router.put('/{user_id}', dependencies=[AdminDep])
async def update_user(
    user_id: int, update_data: UserUpdateFull, uow: DBAnnotation
) -> UserModelWithRoles:
    """Update a user."""
    data = update_data.model_dump(exclude_none=True)
    roles = data.pop('roles')
    updated_user = await UserService.update_user(uow, user_id, data)
    updated_roles = await RoleService.update_roles(uow, user_id, roles)

    new_roles = [role.role for role in updated_roles]
    result = UserModelWithRoles(**updated_user.model_dump(), roles=new_roles)
    return result


@router.delete('/{user_id}', dependencies=[AdminDep])
async def delete_user(user_id: int, uow: DBAnnotation) -> UserModel:
    """Delete a user."""
    user = await UserService.delete_user(uow, user_id)
    result = UserModel(**user.model_dump())
    return result
