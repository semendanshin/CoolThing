import logging

from aiormq import AMQPConnectionError

from config import settings
from infrastructure.mq import RabbitListener
from infrastructure.repositories.beanie import init_db
from infrastructure.repositories.sqlalchemy import session_maker
from infrastructure.repositories.beanie.ScriptsForCampaignRepository import ScriptsForCampaignRepository
from infrastructure.repositories.beanie.ScriptsRepository import ScriptsRepository
from infrastructure.repositories.sqlalchemy.CampaignRepository import CampaignRepository
from infrastructure.repositories.sqlalchemy.WorkersRepository import SQLAlchemyWorkerRepository
from infrastructure.repositories.telegram.TelethonTelegramMessageRepository import TelethonTelegramMessagesRepository
from usecases.CampaignsUseCase import CampaignsUseCase
from usecases.WorkersUseCase import WorkersUseCase
from usecases.ScriptProccessUseCase import ScriptProcessUseCase
from usecases.ScriptsUseCase import ScriptsUseCase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def setup():
    await init_db()


async def log_incoming(message):
    print(f"received: <{type(message)}> {message}")


async def main():
    # scheduler = AsyncIOScheduler()

    await setup()

    scripts_repo = ScriptsRepository()
    scripts_for_campaign_repo = ScriptsForCampaignRepository()

    scripts_use_case = ScriptsUseCase(
        scripts_repository=scripts_repo,
        scripts_for_campaign_repository=scripts_for_campaign_repo,
    )

    workers_repo = SQLAlchemyWorkerRepository(
        session_maker=session_maker,
    )

    messenger = TelethonTelegramMessagesRepository(

    )

    workers_use_case = WorkersUseCase(
        workers=workers_repo,
        messenger=messenger,
    )

    campaigns_repo = CampaignRepository(
        session_maker=session_maker,
    )

    campaigns_use_case = CampaignsUseCase(
        repository=campaigns_repo,
    )

    script_process_use_case = ScriptProcessUseCase(
        scripts_use_case=scripts_use_case,
        workers_use_case=workers_use_case,
        campaign_use_case=campaigns_use_case,
        typing_and_sending_sleep_to=settings.delay.typing_and_sending_sleep_to,
        typing_and_sending_sleep_from=settings.delay.typing_and_sending_sleep_from,
    )

    listener = RabbitListener(
        url=settings.mq.url,
        callback=script_process_use_case.activate_new_script,
    )

    try:
        await listener.start()
    except AMQPConnectionError:
        await listener.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await listener.stop()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
