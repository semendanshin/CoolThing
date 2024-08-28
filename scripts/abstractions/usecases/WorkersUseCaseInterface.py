from abc import ABC, abstractmethod

from domain.models import Worker


class WorkersUseCaseInterface(ABC):
    @abstractmethod
    async def send_message(self, chat_id: str, bot_id: str, message: str):
        ...

    @abstractmethod
    async def get(self, bot_id: str) -> Worker:
        ...
