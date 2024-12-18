from urllib.request import Request

from fastapi import APIRouter

router = APIRouter()


@router.post('/signup')
async def signup(request: Request):
    ...


@router.post('/signin')
async def signin(request: Request):
    ...


@router.put('/signout')
async def signout(request: Request):
    ...


@router.post('/refresh')
async def refresh(request: Request):
    ...
