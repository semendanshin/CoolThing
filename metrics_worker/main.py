from fastapi import FastAPI

from metrics.routes import router

app = FastAPI()
app.include_router(router)
