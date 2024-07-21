from abc import ABC, abstractmethod
from typing import Optional

from domain.chats import Chat, ChatInfo


class AbstractChatsService(ABC):
    @abstractmethod
    async def get_all_chats(self, page: int = 0, size: int = 10) -> list[Optional[ChatInfo]]:
        ...

    @abstractmethod
    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        ...
