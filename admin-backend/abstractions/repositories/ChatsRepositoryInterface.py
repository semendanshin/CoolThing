from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.chat import ChatCreateDTO, ChatUpdateDTO
from domain.models import Chat
from domain.schemas.chats import ChatInfo, Chat as ChatDTO


class ChatsRepositoryInterface(
    CRUDRepositoryInterface[
        Chat, ChatCreateDTO, ChatUpdateDTO,
    ],
    ABC,
):
    @abstractmethod
    async def get_by_worker_id(self, worker_id: str) -> list[Chat]:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[ChatInfo]:
        pass

    @abstractmethod
    async def set_auto_reply(self, chat_id: str, auto_reply: bool) -> None:
        pass

    @abstractmethod
    async def get_dto(self, chat_id: str) -> ChatDTO:
        pass
