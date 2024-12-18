from fastapi import APIRouter

from app.api.accounts import router as account_router
from app.api.authentication import router as auth_router
from app.api.doctor import router as doctor_router

router = APIRouter()

router.include_router(account_router, prefix='/accounts', tags=['Accounts'])
router.include_router(auth_router, prefix='/authentication', tags=['Authentication'])
router.include_router(doctor_router, prefix='/doctors', tags=['Doctors'])
