import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from dependencies.bot import get_bot
from dependencies.bot import setup_application
from infrastructure.repositories.beanie import init_db
from routes import router

logging.basicConfig(
    level=logging.INFO,
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
    await init_db()
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
