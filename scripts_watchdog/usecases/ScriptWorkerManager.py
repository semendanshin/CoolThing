import asyncio
import json
import traceback
import uuid
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path

from aio_pika import IncomingMessage

from abstractions.repositories.container_manager import ContainerManagerInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from domain.events.scripts import NewActiveScript
from domain.worker_settings import WorkerSettings, ScriptToPerform
from settings import settings

logger = getLogger(__name__)

WORKER_IMAGE = "tg-scripts-worker"


@dataclass
class ScriptWorkerManager:
    container_manager: ContainerManagerInterface
    scripts_use_case: ScriptsUseCaseInterface

    tmp_config_dir: Path

    _containers_settings_hashes: dict[str, int] = field(default_factory=dict, init=False)

    # async def execute(self):
    #     workers_settings, running_containers = await asyncio.gather(
    #         self.worker_settings_repository.get_active_bot_settings(),
    #         self.container_manager.get_running_containers()
    #     )
    #
    #     worker_ids = {worker.id for worker in workers_settings}
    #     running_container_ids = {container.id for container in running_containers}
    #
    #     async def process_worker_settings(worker_settings: WorkerSettings):
    #         if worker_settings.id not in self._containers_settings_hashes:
    #             await self.start_worker(worker_settings)
    #         else:
    #             if hash(worker_settings) != self._containers_settings_hashes[worker_settings.id]:
    #                 logger.info(f"Settings for {worker_settings.id} have changed, restarting container")
    #                 await self.stop_container(worker_settings.id)
    #                 await self.start_worker(worker_settings)
    #             if not await self.container_manager.check_health(worker_settings.id):
    #                 logger.warning(f"Container {worker_settings.id} is unhealthy. Restarting...")
    #                 if not await self.container_manager.repair_container(worker_settings.id):
    #                     logger.error(f"Failed to repair container {worker_settings.id}. Stopping...")
    #                     await self.stop_container(worker_settings.id)
    #                     await self.worker_repository.update_status(worker_settings.id, "stopped")
    #
    #     await asyncio.gather(*[process_worker_settings(worker_settings) for worker_settings in workers_settings])
    #     for container_id in running_container_ids - worker_ids:
    #         await self.stop_container(container_id)

    def _make_worker_settings(self, script_to_perform: ScriptToPerform) -> WorkerSettings:
        return WorkerSettings(
            scripts_db=settings.scripts_db,
            mq=settings.mq,
            db=settings.db,
            watcher=settings.watcher,
            notifier=settings.notifier,
            script_to_perform=script_to_perform,
        )

    async def settings_to_file(self, settings: WorkerSettings) -> Path:
        filename = f"{settings.script_to_perform.script_for_campaign_id}.{str(uuid.uuid4())}.json"
        file_path = self.tmp_config_dir / filename

        if isinstance(settings, WorkerSettings):
            structured_settings = settings.model_dump()
        else:
            raise Exception('Settings should be of type WorkerSettings')

        json.dump(
            structured_settings,
            file_path.open("w"),
            indent=4,
            sort_keys=True,
        )

        return file_path

    async def start_worker(self, worker_settings: WorkerSettings):
        settings_file = await self.settings_to_file(worker_settings)

        await self.container_manager.start_container(
            worker_id=worker_settings.script_to_perform.script_for_campaign_id,
            image=WORKER_IMAGE,
            config_path=settings_file
        )

        self._containers_settings_hashes[worker_settings.id] = hash(worker_settings)

    async def stop_container(self, worker_id: str):
        worker_container = await self.container_manager.get_container(worker_id)
        try:
            await self.container_manager.stop_container(worker_id)
        except Exception as e:
            logger.error(f"Error while stopping container {worker_id}: {e}\n{traceback.format_exc()}")
        try:
            worker_container.config_path.unlink()
        except Exception as e:
            logger.error(
                f"Error while removing config file {worker_container.config_path}: {e}\n{traceback.format_exc()}")
        del self._containers_settings_hashes[worker_id]

    async def cleanup(self):
        containers = await self.container_manager.get_running_containers()

        logger.debug(f"Stopping containers: {containers}")

        await asyncio.gather(*[self.stop_container(container.id) for container in containers], return_exceptions=True)

    async def new_activation(self, message: IncomingMessage):
        event = NewActiveScript(**json.loads(message.body.decode()))
        logger.info(f"New script activating request received: {event}")

        sfc = await self.scripts_use_case.get_active_script(sfc_id=event.script_for_campaign_id)

        if sfc.done:
            logger.error(f"SFC {sfc.id} is done, skipping")
            return

        return await self.process_script(event)

    async def process_script(self, event: NewActiveScript):
        dto = ScriptToPerform.model_validate(event)
        settings = self._make_worker_settings(dto)
        await self.start_worker(settings)
