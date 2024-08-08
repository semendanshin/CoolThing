from contextlib import suppress
from dataclasses import dataclass

from abstractions.repositories.TelegramSessionRepositoryInterface import TelegramSessionRepositoryInterface, \
    TwoFARequiredException
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from abstractions.usecases import BotsUseCaseInterface
from domain.dto.worker import WorkerUpdateDTO, WorkerCreateDTO
from domain.models import Worker


@dataclass
class BotsUseCase(
    BotsUseCaseInterface,
):
    async def get_by_username(self, username: str) -> Worker:
        return await self.workers_repo.get_by_username(username)

    session_repo: TelegramSessionRepositoryInterface

    async def send_code(self, app_id: int, app_hash: str, phone: str, proxy: str) -> None:
        await self.session_repo.send_code(app_id, app_hash, phone, proxy)

    async def authorize(self, app_id: int, code: str) -> str:
        with suppress(TwoFARequiredException):
            return await self.session_repo.authorize(app_id, code)
        return ''

    async def authorize_2fa(self, app_id: int, password: str) -> str:
        return await self.session_repo.authorize_2fa(app_id, password)

    workers_repo: WorkersRepositoryInterface

    async def get_bot(self, bot_id: str) -> Worker:
        return await self.workers_repo.get(bot_id)

    async def get_all_bots(self) -> list[Worker]:
        return await self.workers_repo.get_all()

    async def update(self, bot_id: str, schema: WorkerUpdateDTO) -> None:
        await self.workers_repo.update(bot_id, schema)

    async def create(self, schema: WorkerCreateDTO) -> None:
        await self.workers_repo.create(schema)

