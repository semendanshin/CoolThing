import asyncio
import logging
import signal
from logging import getLogger
from pathlib import Path

import docker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from domain.worker_settings import RabbitMQSettings
from infrastructure.repositories.sqlalchemy import SQLAlchemyWorkerRepository
from infrastructure.repositories.sqlalchemy.bot_settings import SQLAlchemyBotSettingsRepository
from infrastructure.repositories.docker.containers import DockerAPIRepository
from settings import settings
from usecases.container_manager import ManageBotsUseCase


logger = getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("docker").setLevel(logging.INFO)


TMP_CONFIG_DIR = Path(__file__).parent / "tmp"
TMP_CONFIG_DIR.mkdir(exist_ok=True)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logger.info("Exiting gracefully")
        self.kill_now = True


async def main():
    scheduler = AsyncIOScheduler()

    client = docker.from_env()

    container_manager = DockerAPIRepository(
        client=client,
        root_config_path=settings.watchdog.root_config_path,
    )

    db_url = (f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}"
              f"@{settings.db.host}:{settings.db.port}/{settings.db.name}")

    logger.info(f"Connecting to database: {settings.db.host}:{settings.db.port}/{settings.db.name}")

    engine = create_async_engine(db_url, echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot_repository = SQLAlchemyBotSettingsRepository(
        session_maker=session_maker,
    )

    worker_repository = SQLAlchemyWorkerRepository(
        session_maker=session_maker,
    )

    manage_bot_use_case = ManageBotsUseCase(
        container_manager=container_manager,
        bot_repository=bot_repository,
        worker_repository=worker_repository,
        rabbit_settings=RabbitMQSettings(
            host=settings.rabbit.host,
            port=settings.rabbit.port,
            user=settings.rabbit.user,
            password=settings.rabbit.password,
            vhost=settings.rabbit.vhost,
        ),
        db_settings=settings.db,
        tmp_config_dir=TMP_CONFIG_DIR,
    )

    scheduler.add_job(
        manage_bot_use_case.execute,
        trigger="interval",
        seconds=settings.watchdog.interval_seconds,
    )

    scheduler.start()

    killer = GracefulKiller()

    while not killer.kill_now:
        await asyncio.sleep(1)

    scheduler.shutdown()

    await manage_bot_use_case.cleanup()

    logger.info("Clean up complete. Exiting.")


if __name__ == "__main__":
    asyncio.run(main())
