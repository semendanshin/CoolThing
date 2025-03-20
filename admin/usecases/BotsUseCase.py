from contextlib import suppress
from dataclasses import dataclass

from matplotlib.style.core import available

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.repositories.TelegramSessionRepositoryInterface import (
    TelegramSessionRepositoryInterface,
    TwoFARequiredException
)
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.usecases import BotsUseCaseInterface
from domain.dto.worker import WorkerUpdateDTO, WorkerCreateDTO
from domain.models import Worker


@dataclass
class BotsUseCase(
    BotsUseCaseInterface,
):
    workers_repo: WorkersRepositoryInterface
    active_scripts_repo: ScriptsForCampaignRepositoryInterface
    session_repo: TelegramSessionRepositoryInterface


    async def get_available_bots(self) -> list[Worker]:
        bots = await self.workers_repo.get_all()

        active_scripts = await self.active_scripts_repo.get_active()

        employed_bots = set()
        for script in active_scripts:
            for username in script.bots_mapping.values():
                employed_bots.add(username)

        available_bots = [x for x in bots if x.username not in employed_bots]
        return available_bots

    async def get_by_username(self, username: str) -> Worker:
        return await self.workers_repo.get_by_username(username)

    async def send_code(self, app_id: int, app_hash: str, phone: str, proxy: str) -> None:
        await self.session_repo.send_code(app_id, app_hash, phone, proxy)

    async def authorize(self, app_id: int, code: str) -> str:
        with suppress(TwoFARequiredException):
            return await self.session_repo.authorize(app_id, code)
        return ''

    async def authorize_2fa(self, app_id: int, password: str) -> str:
        return await self.session_repo.authorize_2fa(app_id, password)

    async def get_bot(self, bot_id: str) -> Worker:
        return await self.workers_repo.get(bot_id)

    async def get_all_bots(self) -> list[Worker]:
        return await self.workers_repo.get_all()

    async def update(self, bot_id: str, schema: WorkerUpdateDTO) -> None:
        await self.workers_repo.update(bot_id, schema)

    async def create(self, schema: WorkerCreateDTO) -> None:
        await self.workers_repo.create(schema)

    async def delete(self, bot_id: str) -> None:
        await self.workers_repo.delete(obj_id=bot_id)
