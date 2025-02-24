import logging
from contextlib import asynccontextmanager
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from dependencies.service import set_service_info
from dependencies.usecases.system import get_system_event_bus
from domain.events.system import Service, ServiceCrashedEvent
from infrastructure.repositories import init_db
from middlewares import check_for_auth
from routes import (dashboard_router, bots_router, bot_router, fallback_router, chats_router,
                    campaigns_router, gpt_settings_router, auth_router, script_router)

logger = logging.getLogger(__name__)

service = Service(
    id=uuid4(),
    name='admin',
    tags=[
        'Admin',
        'User Interactions',
    ]
)

set_service_info(service)

system_event_bus = get_system_event_bus()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("inited db")
    try:
        yield
    except BaseException as e:
        logger.critical(f"Service crashed. Here's why\n\n", exc_info=True)
        crash_event = ServiceCrashedEvent(
            reason=str(e),
        )
        await system_event_bus.publish(crash_event)


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
# app.include_router(bundles_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
