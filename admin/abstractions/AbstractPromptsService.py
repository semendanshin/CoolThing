from abc import ABC, abstractmethod

from domain.prompts import Prompt


class AbstractPromptsService(ABC):
    @abstractmethod
    async def get_all_prompts(self) -> list[Prompt]:
        pass
