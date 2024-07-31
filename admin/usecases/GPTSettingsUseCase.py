from dataclasses import dataclass

from abstractions.repositories.GptSettingsRepositoryInterface import GptSettingsRepositoryInterface
from abstractions.usecases.GPTSettingsUseCaseInterface import GPTSettingsUseCaseInterface
from domain.dto.gpt import GPTCreateDTO, GPTUpdateDTO
from domain.models import GPT


@dataclass
class GPTSettingsUseCase(
    GPTSettingsUseCaseInterface,
):
    repository: GptSettingsRepositoryInterface

    async def get(self, obj_id: str) -> GPT:
        return await self.repository.get(obj_id)

    async def update(self, obj_id: str, schema: GPTUpdateDTO) -> None:
        await self.repository.update(obj_id, schema)

    async def create(self, schema: GPTCreateDTO) -> None:
        await self.repository.create(schema)

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[GPT]:
        return await self.repository.get_all(offset=offset, limit=limit)
