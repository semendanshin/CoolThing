from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.dto.worker import WorkerUpdateDTO, WorkerCreateDTO
from domain.models import Worker


@dataclass
class BotsUseCaseInterface(ABC):
    @abstractmethod
    async def get_bot(self, bot_id: str) -> Worker:
        ...

    @abstractmethod
    async def get_all_bots(self) -> list[Worker]:
        ...

    @abstractmethod
    async def update(self, bot_id: str, schema: WorkerUpdateDTO) -> None:
        ...

    @abstractmethod
    async def send_code(self, app_id: int, app_hash: str, phone: str, proxy: str) -> None:
        ...

    @abstractmethod
    async def authorize(self, app_id: int, code: str) -> str:
        ...

    @abstractmethod
    async def authorize_2fa(self, app_id: int, password: str) -> str:
        ...

    @abstractmethod
    async def create(self, schema: WorkerCreateDTO) -> None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Worker:
        ...

    @abstractmethod
    async def delete(self, bot_id: str) -> None:
        ...

    @abstractmethod
    async def get_available_bots(self) -> list[Worker]:
        ...
