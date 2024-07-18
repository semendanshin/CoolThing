import json
import uuid
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

from abstractions.repositories.bot_settings import BotSettingsRepositoryInterface
from abstractions.repositories.container_manager import ContainerManagerInterface
from abstractions.repositories.worker import WorkerRepositoryInterface
from domain.worker_settings import WorkerSettings, RabbitMQSettings, ManagerSettings, ParserSettings, DBSettings

logger = getLogger(__name__)

MANAGER_IMAGE = "tg-groups-manager"
PARSER_IMAGE = "tg-groups-parser"

TMP_CONFIG_DIR = Path("/tmp/configs")
TMP_CONFIG_DIR.mkdir(exist_ok=True)


@dataclass
class ManageBotsUseCase:
    container_manager: ContainerManagerInterface
    bot_repository: BotSettingsRepositoryInterface
    worker_repository: WorkerRepositoryInterface

    rabbit_settings: RabbitMQSettings
    db_settings: DBSettings

    async def execute(self):
        bots_settings = await self.bot_repository.get_active_bot_settings()

        logger.info(f"Active bots: {bots_settings}")

        actual_bot_ids = [bot.app_id for bot in bots_settings]

        running_containers = await self.container_manager.get_running_containers()
        running_containers_ids = [container.id for container in running_containers]

        bots_to_start = [bot for bot in bots_settings if bot.app_id not in running_containers_ids]
        for bot in bots_to_start:
            logger.debug(f"Starting bot: {bot}")
            await self.start_bot(bot)

        containers_to_stop = [container for container in running_containers if container.id not in actual_bot_ids]
        for container in containers_to_stop:
            await self.container_manager.stop_container(container.id)

        # check health of running containers
        # for container in running_containers:
        #     if not await self.container_manager.check_health(container.id):
        #         await self.container_manager.stop_container(container.id)

    async def _structure_manager_settings(self, manager_settings: ManagerSettings) -> dict:
        return {
            "app": {
                "id": manager_settings.id,
                "api_id": manager_settings.app_id,
                "api_hash": manager_settings.app_hash,
                "session_string": manager_settings.session_string
            },
            "rabbit": {
                "host": self.rabbit_settings.host,
                "port": self.rabbit_settings.port,
                "user": self.rabbit_settings.user,
                "password": self.rabbit_settings.password,
                "vhost": self.rabbit_settings.vhost,
                "queue": manager_settings.topic
            },
            "openai": {
                "model": manager_settings.model,
                "api_key": manager_settings.token,
            },
            "db": {
                "host": self.db_settings.host,
                "port": self.db_settings.port,
                "user": self.db_settings.user,
                "password": self.db_settings.password,
                "name": self.db_settings.name
            },
            "welcome_message": manager_settings.welcome_message
        }

    async def _structure_parser_settings(self, parser_settings: ParserSettings) -> dict:
        return {
            "app": {
                "id": parser_settings.id,
                "api_id": parser_settings.app_id,
                "api_hash": parser_settings.app_hash,
                "session_string": parser_settings.session_string
            },
            "rabbit": {
                "host": self.rabbit_settings.host,
                "port": self.rabbit_settings.port,
                "user": self.rabbit_settings.user,
                "password": self.rabbit_settings.password,
                "vhost": self.rabbit_settings.vhost,
                "queue": parser_settings.topic
            },
            "parser": {
                "keywords": {
                    "positive": parser_settings.plus_keywords,
                    "negative": parser_settings.minus_keywords
                },
                "chats": parser_settings.chats
            }
        }

    async def settings_to_file(self, settings: WorkerSettings) -> Path:
        filename = f"{settings.app_id}.{str(uuid.uuid4())}.json"
        file_path = TMP_CONFIG_DIR / filename

        if isinstance(settings, ManagerSettings):
            structured_settings = await self._structure_manager_settings(settings)
        elif isinstance(settings, ParserSettings):
            structured_settings = await self._structure_parser_settings(settings)
        else:
            structured_settings = {}

        json.dump(
            structured_settings,
            file_path.open("w"),
            indent=4,
            sort_keys=True,
        )

        return file_path

    async def start_bot(self, bot_settings: WorkerSettings):
        if bot_settings.role not in ["manager", "parser"]:
            raise ValueError("Unknown bot role")

        # create settings file from bot settings and rabbit settings
        settings_file = await self.settings_to_file(bot_settings)

        # start container
        container_id = await self.container_manager.start_container(
            worker_id=bot_settings.app_id,
            image=MANAGER_IMAGE if bot_settings.role == "manager" else PARSER_IMAGE,
            config_path=settings_file
        )

        # update bot status
        # await self.worker_repository.update_status(bot_settings.app_id, "running")

    async def cleanup(self):
        containers = await self.container_manager.get_running_containers()
        for container in containers:
            await self.container_manager.stop_container(container.id)
