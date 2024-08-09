from abc import ABC, abstractmethod

from domain.schemas.prompts import Prompt


class PromptsUseCaseInterface(ABC):
    @abstractmethod
    async def get_all_prompts(self) -> list[Prompt]:
        pass
