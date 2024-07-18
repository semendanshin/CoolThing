from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path

from docker import DockerClient
from docker.types import Mount
from abstractions.repositories.container_manager import ContainerManagerInterface, Bot


logger = getLogger(__name__)


@dataclass
class DockerAPIRepository(ContainerManagerInterface):

    client: DockerClient

    config_file_destination: Path = Path("/app/settings.json")

    _containers: dict[str, Bot] = field(default_factory=dict)

    async def start_container(self, worker_id: str, image: str, config_path: Path) -> str:
        if not config_path.is_absolute():
            config_path = Path(__file__).parent / config_path

        logger.info(f"Starting container with image {image} and config {config_path}")

        container = self.client.containers.run(
            image=image,
            mounts=[
                Mount(
                    target=str(self.config_file_destination),
                    source=str(config_path),
                    type="bind",
                    read_only=True
                )
            ],
            detach=True,
            network_mode="host",
            auto_remove=True,
        )

        # wait for container to start
        container.reload()
        while container.status != "running":
            container.reload()

        bot = Bot(
            id=worker_id,
            name=container.name,
            status=container.status,
            config_path=config_path,
            container_id=container.id
        )

        self._containers[worker_id] = bot

        return container.id

    async def stop_container(self, worker_id: str) -> None:
        logger.info(f"Stopping container {worker_id}")
        bot = self._containers.pop(worker_id, None)
        if not bot:
            return
        container = self.client.containers.get(bot.container_id)
        container.stop()
        container.remove()

    async def get_running_containers(self) -> list[Bot]:
        return list(self._containers.values())

    async def check_health(self, worker_id: str) -> bool:
        bot = self._containers.get(worker_id)
        if not bot:
            return False

        container = self.client.containers.get(bot.container_id)
        return container.status == "running"
