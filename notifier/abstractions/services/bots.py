from abc import abstractmethod, ABC
from dataclasses import dataclass
from uuid import UUID

from domain.models import Worker


@dataclass
class BotsServiceInterface(ABC):
    @abstractmethod
    async def get_bot(self, bot_id: UUID) -> Worker:
        ...
