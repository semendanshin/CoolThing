import asyncio
import signal
from dataclasses import field, dataclass
from pathlib import Path

import docker
from docker.models.containers import Container
from docker.types import Mount

client = docker.from_env()


@dataclass
class ContainerManager:
    image: str

    config_file_destination: Path = Path("/app/settings.json")

    _containers: dict[str, Container] = field(default_factory=dict)

    async def new_container(self, name: str, config_file_path: Path):
        if not config_file_path.is_absolute():
            config_file_path = Path(__file__).parent / config_file_path
        container = client.containers.run(
            image=self.image,
            mounts=[
                Mount(
                    target=str(self.config_file_destination),
                    source=str(config_file_path),
                    type="bind",
                    read_only=True
                )
            ],
            detach=True,
            name=name,
            network_mode="host",
            auto_remove=True,
        )
        self._containers[name] = container

    async def stop_container(self, name: str):
        container = self._containers.pop(name)
        container.stop()
        container.remove()

    async def stop_all_containers(self):
        for name in list(self._containers):
            await self.stop_container(name)

    async def check_health(self, name: str):
        container = self._containers[name]
        return container.status == "running"

    async def repair(self, name: str):
        container = self._containers[name]
        if container.status != "running":
            container.start()

    async def watchdog(self):
        while self._containers:
            for name in list(self._containers):
                if not await self.check_health(name):
                    await self.repair(name)
            await asyncio.sleep(5)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


async def main():
    manager1 = ContainerManager("tg-groups-parser")
    manager2 = ContainerManager("tg-groups-manager")

    await manager1.new_container("parser1", Path("1.settings.json"))
    await manager2.new_container("manager1", Path("2.settings.json"))

    task1 = asyncio.create_task(manager1.watchdog())
    task2 = asyncio.create_task(manager2.watchdog())

    killer = GracefulKiller()
    while not killer.kill_now:
        await asyncio.sleep(1)

    await manager1.stop_all_containers()
    await manager2.stop_all_containers()

    task1.cancel()
    task2.cancel()

if __name__ == "__main__":
    asyncio.run(main())
