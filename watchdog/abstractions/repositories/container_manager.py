from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class WorkerContainer:
    id: str
    config_path: Path
    restarts: int = 0
    container_id: str = None


class ContainerManagerInterface(ABC):
    @abstractmethod
    async def get_container(self, worker_id: str) -> WorkerContainer:
        pass

    @abstractmethod
    async def start_container(self, worker_id: str, image: str, config_path: Path) -> None:
        pass

    @abstractmethod
    async def stop_container(self, worker_id: str) -> None:
        pass

    @abstractmethod
    async def get_running_containers(self) -> list[WorkerContainer]:
        pass

    @abstractmethod
    async def check_health(self, worker_id: str) -> bool:
        pass

    @abstractmethod
    async def repair_container(self, worker_id: str) -> bool:
        pass
