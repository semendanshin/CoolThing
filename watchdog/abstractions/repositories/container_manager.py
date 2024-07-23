from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Bot:
    id: str
    name: str
    status: str
    config_path: Path
    container_id: str = None
    settings_hash: str = None


class ContainerManagerInterface(ABC):
    @abstractmethod
    async def start_container(self, worker_id: str, image: str, config_path: Path) -> None:
        pass

    @abstractmethod
    async def stop_container(self, worker_id: str) -> None:
        pass

    @abstractmethod
    async def get_running_containers(self) -> list[Bot]:
        pass
