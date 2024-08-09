from abc import abstractmethod, ABC

from domain.dto.gpt import GPTCreateDTO, GPTUpdateDTO
from domain.models import GPT


class GPTSettingsUseCaseInterface(ABC):
    @abstractmethod
    async def get(self, settings_id: str) -> GPT:
        ...

    @abstractmethod
    async def update(self, settings_id: str, schema: GPTUpdateDTO) -> None:
        ...

    @abstractmethod
    async def create(self, schema: GPTCreateDTO) -> None:
        ...

    @abstractmethod
    async def get_all(self, offset: int = 0, limit: int = 10) -> list[GPT]:
        ...

    @abstractmethod
    async def delete(self, settings_id: str) -> None:
        ...
