import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import main_router
from app.core.settings import settings
from app.exceptions.handlers import add_exception_handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router, prefix='/api')

add_exception_handlers(app)

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
