import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from infrastructure.repositories import init_db
from middlewares import check_for_auth
from routes import (dashboard_router, bots_router, bot_router, fallback_router, chats_router,
                    campaigns_router, gpt_settings_router, auth_router, script_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logging.getLogger(__name__).info("inited db")
    yield


app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.middleware('http')(check_for_auth)

app.include_router(dashboard_router)
app.include_router(bots_router)
app.include_router(bot_router)
app.include_router(fallback_router)
# app.include_router(prompts_router)
app.include_router(chats_router)
app.include_router(campaigns_router)
app.include_router(gpt_settings_router)
app.include_router(auth_router)
app.include_router(script_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
    # uvicorn.run(app, host='0.0.0.0', port=8080)
