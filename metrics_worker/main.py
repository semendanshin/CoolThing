import logging

from fastapi import FastAPI

from metrics.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
app = FastAPI()
app.include_router(router)
