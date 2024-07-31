from dataclasses import dataclass

from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.repositories.GptSettingsRepositoryInterface import GptSettingsRepositoryInterface
from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from abstractions.usecases import BotsUseCaseInterface
from domain.models import Worker as WorkerModel, Worker
from domain.models import Campaign as CampaignModel
from domain.models import Chat as ChatModel
from domain.models import GPT as GPTModel
from domain.schemas.bots import ManagerBotDetails, ParserBotDetails, ManagerBotOverview, ParserBotOverview


@dataclass
class BotsUseCase(
    BotsUseCaseInterface,
):
    workers_repo: WorkersRepositoryInterface

    async def get_bot(self, bot_id: str) -> Worker:
        return await self.workers_repo.get(bot_id)

    async def get_manager_bots(self) -> list[Worker]:
        return await self.workers_repo.get_by_role('manager')

    async def get_parser_bots(self) -> list[Worker]:
        return await self.workers_repo.get_by_role('parser')

    async def connect_bot_by_code(self, code: str) -> bool:
        pass

    async def connect_bot_by_password(self, password: str) -> bool:
        pass
