from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_doctors():
    ...


@router.get('/{id}')
async def get_doctor(id: str):
    ...
