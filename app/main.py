from fastapi import FastAPI

import uvicorn


app = FastAPI()

@app.get('/')
def helo():
    return 'helo'

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)