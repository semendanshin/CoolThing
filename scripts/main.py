import logging
from uuid import UUID

from aiormq import AMQPConnectionError

from config import settings
from domain.reports.notifier import Service
from infrastructure.mq import RabbitListener
from infrastructure.repositories.beanie import init_db
from infrastructure.repositories.beanie.ScriptsForCampaignRepository import ScriptsForCampaignRepository
from infrastructure.repositories.beanie.ScriptsRepository import ScriptsRepository
from infrastructure.repositories.sqlalchemy import session_maker
from infrastructure.repositories.sqlalchemy.CampaignRepository import CampaignRepository
from infrastructure.repositories.sqlalchemy.WorkersRepository import SQLAlchemyWorkerRepository
from infrastructure.repositories.telegram.TelethonTelegramMessageRepository import TelethonTelegramMessagesRepository
from usecases.CampaignsUseCase import CampaignsUseCase
from usecases.ScriptProccessUseCase import ScriptProcessUseCase
from usecases.ScriptsUseCase import ScriptsUseCase
from usecases.TemplateEngine import TemplateEngine
from usecases.WorkersUseCase import WorkersUseCase
from usecases.notificator import Notificator
from usecases.watcher import Watcher

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

    service_identity = Service(
        id=UUID('7931b22f-7f3c-482a-9961-558be2069b04'),
        name='scripts',
        tags=['Script', 'Process']
    )

    notificator = Notificator(
        service=service_identity,
        base_url=settings.notifier.base_url,
    )

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

    template_engine = TemplateEngine(

    )

    watcher = Watcher(
        base_url=settings.watcher.base_url,
        new_activation_endpoint=settings.watcher.new_activation_endpoint,
        target_chats_endpoint=settings.watcher.target_chats_endpoint,
        script_status_endpoint=settings.watcher.script_status_endpoint,
        chat_status_endpoint=settings.watcher.chat_status_endpoint,
        message_status_endpoint=settings.watcher.message_status_endpoint,
        notificator=notificator,
    )

    script_process_use_case = ScriptProcessUseCase(
        scripts_use_case=scripts_use_case,
        workers_use_case=workers_use_case,
        campaign_use_case=campaigns_use_case,
        template_engine=template_engine,
        watcher=watcher,
    )

    listener = RabbitListener(
        url=settings.mq.url,
        callback=script_process_use_case.activate_new_script,
    )

    try:
        await listener.start()
    except AMQPConnectionError:
        await asyncio.sleep(5)
        await listener.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await listener.stop()
    except Exception as e:
        logger.error("Unhandled exception occurred", exc_info=True)


    finally:
        await listener.stop()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
