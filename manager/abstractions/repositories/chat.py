from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from abstractions.repositories import CRUDRepositoryInterface
from domain.models import Chat


@dataclass
class ChatCreateDTO:
    id: str
    campaign_id: str
    telegram_chat_id: int
    worker_id: str
    username: str
    status: str
    lead_message: str
    lead_chat_id: str


@dataclass
class ChatUpdateDTO:
    pass


class ChatRepositoryInterface(
    CRUDRepositoryInterface[Chat, ChatCreateDTO, ChatUpdateDTO], ABC
):
    @abstractmethod
    async def get_by_telegram_chat_id(self, telegram_chat_id: int) -> Optional[Chat]:
        pass

    @abstractmethod
    async def get_by_worker_id(self, worker_id: str) -> list[Chat]:
        pass
