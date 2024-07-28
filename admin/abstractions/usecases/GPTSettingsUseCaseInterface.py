from abc import abstractmethod, ABC

from domain.dto.gpt import GPTCreateDTO, GPTUpdateDTO
from domain.models import GPT


class GPTSettingsUseCaseInterface(ABC):
    @abstractmethod
    async def get(self, campaign_id: str) -> GPT:
        ...

    @abstractmethod
    async def update(self, campaign_id: str, schema: GPTUpdateDTO) -> None:
        ...

    @abstractmethod
    async def create(self, schema: GPTCreateDTO) -> None:
        ...

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[GPT]:
        ...
