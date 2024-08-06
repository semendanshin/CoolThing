from abc import ABC, abstractmethod
from typing import Annotated


class MessageHelperInterface(ABC):
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
