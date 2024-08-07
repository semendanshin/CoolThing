import asyncio
import json
import traceback
import uuid
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path

from abstractions.repositories.bot_settings import BotSettingsRepositoryInterface
from abstractions.repositories.container_manager import ContainerManagerInterface
from abstractions.repositories.worker import WorkerRepositoryInterface
from domain.worker_settings import WorkerSettings, RabbitMQSettings, ManagerSettings, ParserSettings, DBSettings

logger = getLogger(__name__)

MANAGER_IMAGE = "tg-groups-manager"
PARSER_IMAGE = "tg-groups-parser"


@dataclass
class ManageBotsUseCase:
    container_manager: ContainerManagerInterface
    worker_settings_repository: BotSettingsRepositoryInterface
    worker_repository: WorkerRepositoryInterface

    rabbit_settings: RabbitMQSettings
    db_settings: DBSettings
    batching_sleep: int

    tmp_config_dir: Path

    _containers_settings_hashes: dict[str, int] = field(default_factory=dict, init=False)

    async def execute(self):
        print("executing")
        workers_settings, running_containers = await asyncio.gather(
            self.worker_settings_repository.get_active_bot_settings(),
            self.container_manager.get_running_containers()
        )

        print("got settings and containers")

        worker_ids = {worker.id for worker in workers_settings}
        running_container_ids = {container.id for container in running_containers}
        print(worker_ids, running_container_ids)

        async def process_worker_settings(worker_settings: WorkerSettings):
            if worker_settings.id not in self._containers_settings_hashes:
                await self.start_bot(worker_settings)
            else:
                if hash(worker_settings) != self._containers_settings_hashes[worker_settings.id]:
                    logger.info(f"Settings for {worker_settings.id} have changed, restarting container")
                    await self.stop_container(worker_settings.id)
                    await self.start_bot(worker_settings)
                if not await self.container_manager.check_health(worker_settings.id):
                    logger.warning(f"Container {worker_settings.id} is unhealthy. Restarting...")
                    if not await self.container_manager.repair_container(worker_settings.id):
                        logger.error(f"Failed to repair container {worker_settings.id}. Stopping...")
                        await self.stop_container(worker_settings.id)
                        await self.worker_repository.update_status(worker_settings.id, "stopped")

        await asyncio.gather(*[process_worker_settings(worker_settings) for worker_settings in workers_settings])
        for container_id in running_container_ids - worker_ids:
            await self.stop_container(container_id)

    async def _structure_manager_settings(self, manager_settings: ManagerSettings) -> dict:
        return {
            "app": {
                "id": manager_settings.id,
                "api_id": manager_settings.app_id,
                "api_hash": manager_settings.app_hash,
                "session_string": manager_settings.session_string,
                "proxy": manager_settings.proxy,
            },
            "rabbit": {
                "host": self.rabbit_settings.host,
                "port": self.rabbit_settings.port,
                "user": self.rabbit_settings.user,
                "password": self.rabbit_settings.password,
                "vhost": self.rabbit_settings.vhost,
            },
            "openai": {
                "model": manager_settings.model,
                "api_key": manager_settings.token,
                "service_prompt": manager_settings.service_prompt,
                "assistant": manager_settings.assistant,
                "proxy": manager_settings.openai_proxy,
            },
            "db": {
                "host": self.db_settings.host,
                "port": self.db_settings.port,
                "user": self.db_settings.user,
                "password": self.db_settings.password,
                "name": self.db_settings.name
            },
            "welcome_message": manager_settings.welcome_message,
            "campaign_id": manager_settings.campaign_id,
            "batch": {
                "typing_and_sending_sleep_from": manager_settings.typing_and_sending_sleep_from,
                "typing_and_sending_sleep_to": manager_settings.typing_and_sending_sleep_to,
                "welcome_sleep_from": manager_settings.welcome_sleep_from,
                "welcome_sleep_to": manager_settings.welcome_sleep_to,
                "batching_sleep": self.batching_sleep
            },
        }

    async def _structure_parser_settings(self, parser_settings: ParserSettings) -> dict:
        return {
            "app": {
                "id": parser_settings.id,
                "api_id": parser_settings.app_id,
                "api_hash": parser_settings.app_hash,
                "session_string": parser_settings.session_string,
                "proxy": parser_settings.proxy,
            },
            "rabbit": {
                "host": self.rabbit_settings.host,
                "port": self.rabbit_settings.port,
                "user": self.rabbit_settings.user,
                "password": self.rabbit_settings.password,
                "vhost": self.rabbit_settings.vhost,
                "campaign_id": parser_settings.campaign_id,
            },
            "parser": {
                "keywords": {
                    "positive": parser_settings.plus_keywords,
                    "negative": parser_settings.minus_keywords
                },
                "chats": parser_settings.chats
            },
            "debug": True,
        }

    async def settings_to_file(self, settings: WorkerSettings) -> Path:
        filename = f"{settings.id}.{str(uuid.uuid4())}.json"
        file_path = self.tmp_config_dir / filename

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

        settings_file = await self.settings_to_file(bot_settings)

        await self.container_manager.start_container(
            worker_id=bot_settings.id,
            image=MANAGER_IMAGE if bot_settings.role == "manager" else PARSER_IMAGE,
            config_path=settings_file
        )

        self._containers_settings_hashes[bot_settings.id] = hash(bot_settings)

    async def stop_container(self, worker_id: str):
        worker_container = await self.container_manager.get_container(worker_id)
        try:
            await self.container_manager.stop_container(worker_id)
        except Exception as e:
            logger.error(f"Error while stopping container {worker_id}: {e}\n{traceback.format_exc()}")
        try:
            worker_container.config_path.unlink()
        except Exception as e:
            logger.error(f"Error while removing config file {worker_container.config_path}: {e}\n{traceback.format_exc()}")
        del self._containers_settings_hashes[worker_id]

    async def cleanup(self):
        containers = await self.container_manager.get_running_containers()

        logger.debug(f"Stopping containers: {containers}")

        await asyncio.gather(*[self.stop_container(container.id) for container in containers], return_exceptions=True)
