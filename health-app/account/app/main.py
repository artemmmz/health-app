import uvicorn
from fastapi import FastAPI

from app.api import main_router

app = FastAPI()
app.include_router(main_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000)
