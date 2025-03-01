import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.repositories.beanie import init_db
from metrics.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield  # После yield FastAPI продолжит работу, а при завершении приложения — выполнит завершающую часть (если нужна)


app = FastAPI(lifespan=lifespan)

app.include_router(router)
