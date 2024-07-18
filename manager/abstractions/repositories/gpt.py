from abc import ABC, abstractmethod

from domain.models import Message


class GPTRepositoryInterface(ABC):
    @abstractmethod
    async def generate_response(self, messages: list[Message]) -> str:
        raise NotImplementedError
