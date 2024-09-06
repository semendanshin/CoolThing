from abc import ABC, abstractmethod
from typing import Annotated


class TelegramClientWrapper(ABC):
    @abstractmethod
    async def get_chat_id(
            self,
            username: str,
    ) -> int:
        ...

    @abstractmethod
    async def get_username_by_chat_id(
            self,
            chat_id: int,
    ) -> str:
        ...

    @abstractmethod
    async def set_typing_status(
            self,
            chat_id: int,
    ) -> None:
        ...

    @abstractmethod
    async def send_message(
            self,
            chat_id: int,
            text: str,
    ) -> None:
        ...
