from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path
from typing import Any

from aiodocker import Docker

from abstractions.repositories.container_manager import ContainerManagerInterface, WorkerContainer

logger = getLogger(__name__)


@dataclass
class AsyncDockerAPIRepository(ContainerManagerInterface):
    client: Docker

    root_config_path: Path

    network_name: str = "coolthing_bridge"
    config_file_destination: Path = Path("/app/settings.json")
    fluentd_address: str = "localhost:24224"

    max_restarts: int = 3

    _containers: dict[str, WorkerContainer] = field(default_factory=dict)

    async def get_container(self, worker_id: str) -> WorkerContainer:
        return self._containers.get(worker_id)

    async def start_container(self, worker_id: str, image: str, config_path: Path) -> None:
        logger.info(f"Starting container with image {image} and config {config_path}")

        container_name = f"{image}-{worker_id}"
        container = await self.client.containers.create_or_replace(
            name=container_name,
            config=self._get_container_config(image, config_path, worker_id)
        )
        await container.start()

        network = await self.client.networks.get("infrastructure")
        await network.connect({"Container": container.id})

        network = await self.client.networks.get("monitoring")
        await network.connect({"Container": container.id})

        bot = WorkerContainer(
            id=worker_id,
            config_path=config_path,
            container_id=container.id
        )

        self._containers[worker_id] = bot

        return container.id

    def _get_container_config(self, image: str, config_path: Path, worker_id: str) -> dict[str, Any]:
        return {
            "Image": image,
            "HostConfig": {
                "Binds": [
                    f"{self.root_config_path / config_path.name}:{self.config_file_destination}:ro"
                ],
                "LogConfig": {
                    "Type": "fluentd",
                    "Config": {
                        "fluentd-address": self.fluentd_address,
                        "tag": "{0}.{1}".format(image, worker_id)
                    },
                },
                "NetworkMode": self.network_name,
            },
            "Mounts": [
                {
                    "Type": "bind",
                    "Source": str(self.root_config_path / config_path.name),
                    "Destination": str(self.config_file_destination),
                    "Mode": "ro"
                }
            ],
        }

    async def stop_container(self, worker_id: str) -> None:
        logger.info(f"Stopping container {worker_id}")
        bot = self._containers.pop(worker_id, None)
        if not bot:
            return
        container = await self.client.containers.get(
            container_id=bot.container_id
        )
        await container.delete(force=True)

    async def get_running_containers(self) -> list[WorkerContainer]:
        return list(self._containers.values())

    async def check_health(self, worker_id: str) -> bool:
        bot = self._containers.get(worker_id)
        if not bot:
            return False
        container = await self.client.containers.get(
            container_id=bot.container_id
        )
        data = await container.show()
        return data.get("State", {}).get("Running", False)

    async def repair_container(self, worker_id: str) -> bool:
        bot = self._containers.get(worker_id)
        if not bot:
            return False
        container = await self.client.containers.get(
            container_id=bot.container_id
        )
        if not await self.check_health(worker_id):
            if bot.restarts >= self.max_restarts:
                return False
            bot.restarts += 1
            await container.restart()
        return True
