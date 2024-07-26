from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.chat import ChatCreateDTO, ChatUpdateDTO
from domain.models import Chat


class ChatsRepositoryInterface(
    CRUDRepositoryInterface[
        Chat, ChatCreateDTO, ChatUpdateDTO,
    ],
    ABC,
):
    @abstractmethod
    async def get_by_worker_id(self, worker_id: str) -> list[Chat]:
        pass
