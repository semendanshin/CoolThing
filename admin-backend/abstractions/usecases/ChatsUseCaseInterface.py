from abc import ABC, abstractmethod
from typing import Optional

from domain.schemas.chats import Chat, ChatInfo


class ChatsUseCaseInterface(ABC):
    @abstractmethod
    async def get_all_chats(self, offset: int = 0, limit: int = 10) -> list[ChatInfo]:
        ...

    @abstractmethod
    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        ...

    @abstractmethod
    async def send_message(self, chat_id: str, message: str) -> None:
        ...

    @abstractmethod
    async def set_auto_reply(self, chat_id: str, auto_reply: bool) -> None:
        ...
