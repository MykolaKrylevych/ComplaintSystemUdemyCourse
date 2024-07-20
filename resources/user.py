from typing import Optional, List

from fastapi import APIRouter, Depends
from managers.user import UserManager
from managers.auth import oauth2_scheme, is_admin
from schemas.response.user import UserOut
from models import RoleType

router = APIRouter(tags=["Users"])


@router.get(
    "/users/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=List[UserOut],
)
async def get_all_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_by_email(email)
    return await UserManager.get_all_users()


@router.put(
    "/users/{user_id}/make_admin",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int):
    await UserManager.change_role(RoleType.admin, user_id)


@router.put(
    "/users/{user_id}/make_approver",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int):
    await UserManager.change_role(RoleType.approver, user_id)
