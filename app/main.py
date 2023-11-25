from fastapi import FastAPI

import uvicorn

from app.routers.auth import auth_router
from app.routers.registrate import reg_router
from app.routers.track import track_router

app = FastAPI()


app.include_router(reg_router)
app.include_router(auth_router, tags=['Auth'], prefix='/login')
app.include_router(track_router)

@app.get('/')
def helo():
    return 'helo'

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)