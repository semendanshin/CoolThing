from abc import ABC, abstractmethod

from domain.models import Worker


class WorkersUseCaseInterface(ABC):
    @abstractmethod
    async def send_message(self, chat_id: str, bot_id: str, message: str, reply_to: int) -> int:
        ...

    @abstractmethod
    async def get(self, bot_id: str) -> Worker:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Worker:
        ...
