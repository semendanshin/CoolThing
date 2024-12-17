import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from infrastructure.repositories.beanie import init_db
from routes import process_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(_) -> AsyncGenerator[None, None]:
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(process_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
