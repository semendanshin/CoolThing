import asyncio
import logging
from os import getenv

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from seed import seed
from models import Script, ScriptForCampaign

from dotenv import load_dotenv

load_dotenv()

MONGO_INITDB_ROOT_USERNAME = getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = getenv('MONGO_INITDB_ROOT_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')

logger = logging.getLogger(__name__)


async def init_db():
    try:
        connection_string = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{DB_HOST}:{DB_PORT}/"
        client = AsyncIOMotorClient(connection_string)
        await init_beanie(
            database=client[DB_NAME],
            document_models=[
                Script,
                ScriptForCampaign
            ]
        )
        logger.info("DB initialized")
        print("DB initialized")
        print(client.scripts)
    except Exception as e:
        print(e)


async def main():
    await init_db()
    await seed()


if __name__ == '__main__':
    asyncio.run(main())
