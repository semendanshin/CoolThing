import logging
from pathlib import Path

import aiodocker
from aiormq import AMQPConnectionError

from infrastructure.mq import RabbitListener
from infrastructure.repositories.beanie import init_db
from infrastructure.repositories.beanie.ScriptsForCampaignRepository import ScriptsForCampaignRepository
from infrastructure.repositories.beanie.ScriptsRepository import ScriptsRepository
from infrastructure.repositories.docker import AsyncDockerAPIRepository
from settings import settings
from usecases.ScriptWorkerManager import ScriptWorkerManager
from usecases.ScriptsUseCase import ScriptsUseCase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

TMP_CONFIG_DIR = Path(__file__).parent / "tmp"
TMP_CONFIG_DIR.mkdir(exist_ok=True)


async def setup():
    await init_db()


async def log_incoming(message):
    print(f"received: <{type(message)}> {message}")


async def main():
    await setup()

    # service_identity = Service(
    #     id=UUID('7931b22f-7f3c-482a-9961-558be2069b04'),
    #     name='scripts',
    #     tags=['Script', 'Process']
    # )

    # notificator = Notificator(
    #     service=service_identity,
    #     base_url=settings.notifier.base_url,
    # )

    scripts_repo = ScriptsRepository()
    scripts_for_campaign_repo = ScriptsForCampaignRepository()

    scripts_use_case = ScriptsUseCase(
        scripts_repository=scripts_repo,
        scripts_for_campaign_repository=scripts_for_campaign_repo,
    )

    client = aiodocker.Docker()

    container_manager = AsyncDockerAPIRepository(
        client=client,
        root_config_path=settings.watchdog.root_config_path,
    )

    script_worker_manager = ScriptWorkerManager(
        container_manager=container_manager,
        scripts_use_case=scripts_use_case,
        tmp_config_dir=TMP_CONFIG_DIR,
    )

    listener = RabbitListener(
        url=settings.mq.url,
        callback=script_worker_manager.new_activation,
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
