from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_me():
    ...


@router.post('/update')
async def update_me():
    ...


@router.post('/')
async def get_all():
    ...


@router.post('/')
async def create():
    ...


@router.put('/{id}')
async def update(id):
    ...


@router.delete('/{id}')
async def delete(id):
    ...
