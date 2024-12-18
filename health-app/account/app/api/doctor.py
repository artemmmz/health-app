from typing import List, Annotated

from fastapi import APIRouter, Query

from app.core.dependencies import UserDep, DBAnnotation
from app.exceptions import NoResultError
from app.models.user_models import DoctorGet, UserModel
from app.services import RoleService, UserService
from app.utils.enums import Role

router = APIRouter()


@router.get('/', dependencies=[UserDep])
async def get_doctors(
    data: Annotated[DoctorGet, Query()], uow: DBAnnotation
) -> List[UserModel]:
    """Get all doctors."""
    user_roles = await RoleService.get_all_roles(uow, [Role.DOCTOR])
    user_ids = [user_roles.user_id for user_roles in user_roles]

    doctors = await UserService.get_users_by_ids(
        uow,
        user_ids,
        offset=data.from_,
        limit=data.count,
        full_name=data.name_filter,
    )
    result = []
    for doctor in doctors:
        result.append(UserModel(**doctor.model_dump()))
    return result


@router.get('/{user_id}', dependencies=[UserDep])
async def get_doctor(user_id: int, uow: DBAnnotation) -> UserModel:
    """Get a doctor by id."""
    try:
        await RoleService.get_role(uow, user_id, Role.DOCTOR)
    except NoResultError:
        raise NoResultError('Doctor')
    doctor = await UserService.get_user_by_id(uow, user_id)
    return UserModel(**doctor.model_dump())
