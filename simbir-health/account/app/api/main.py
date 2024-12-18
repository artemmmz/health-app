from fastapi import APIRouter

subrouters = []

router = APIRouter()

for subrouter in subrouters:
    router.include_router(subrouter)
