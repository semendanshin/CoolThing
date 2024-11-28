import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from dependencies.bot import get_bot
from dependencies.bot import setup_application
from routes import router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

bot = get_bot()
bot_application = setup_application()


@asynccontextmanager
async def lifespan(_) -> AsyncGenerator[None, None]:
    await bot_application.initialize()

    await bot_application.start()
    await bot_application.updater.start_polling()  # noqa
    logger.info('Telegram bot started')
    yield
    await bot_application.updater.stop()  # noqa
    await bot_application.stop()
    logger.info('Telegram bot stopped')


def build_app() -> FastAPI:
    fast_api_app = FastAPI(lifespan=lifespan)
    fast_api_app.include_router(router)
    return fast_api_app


app = build_app()
