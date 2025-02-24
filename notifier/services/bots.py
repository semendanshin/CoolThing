from dataclasses import dataclass
from uuid import UUID

from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.services.bots import BotsServiceInterface
from domain.models import Worker


@dataclass
class BotsService(BotsServiceInterface):
    workers: WorkersRepositoryInterface

    async def get_bot(self, bot_id: UUID) -> Worker:
        return await self.workers.get(obj_id=str(bot_id))
