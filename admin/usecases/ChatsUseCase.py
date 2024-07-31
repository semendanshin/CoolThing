from dataclasses import dataclass
from typing import Optional

from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from abstractions.usecases import ChatsUseCaseInterface
from domain.schemas.chats import Chat, ChatInfo


@dataclass
class ChatsUseCase(ChatsUseCaseInterface):
    repository: ChatsRepositoryInterface

    async def get_all_chats(self, offset: int = 0, limit: int = 10) -> list[ChatInfo]:
        return await self.repository.get_all(offset=offset, limit=limit)

    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        return await self.repository.get(chat_id)
