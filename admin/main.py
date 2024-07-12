import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import dashboard_router, bots_router, fallback_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(dashboard_router)
app.include_router(bots_router)
app.include_router(fallback_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
