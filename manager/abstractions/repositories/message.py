import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from abstractions.repositories import CRUDRepositoryInterface
from domain.models import Message


@dataclass(kw_only=True)
class MessageCreateDTO:
    id: str = field(default_factory=lambda : str(uuid.uuid4()))
    chat_id: str
    text: str
    is_outgoing: bool


@dataclass
class MessageUpdateDTO:
    pass


class MessageRepositoryInterface(
    CRUDRepositoryInterface[Message, MessageCreateDTO, MessageUpdateDTO], ABC
):
    @abstractmethod
    async def get_by_chat_id(self, chat_id: str, limit: int = 10, offset: int = 0) -> list[Message]:
        pass
