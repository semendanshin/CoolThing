import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings
from infrastructure.entities.beanie import Script, ScriptForCampaign, ActiveScriptProcess

logger = logging.getLogger(__name__)


async def init_db():
    try:
        connection_string = settings.scripts_db.url
        client = AsyncIOMotorClient(connection_string)
        await init_beanie(
            database=client[settings.scripts_db.name],
            document_models=[
                Script,
                ScriptForCampaign,
                ActiveScriptProcess,
            ]
        )
        logger.info("DB initialized")
    except Exception as e:
        logger.exception(e, exc_info=True)
