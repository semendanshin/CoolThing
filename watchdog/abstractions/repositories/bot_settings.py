from abc import ABC, abstractmethod

from domain.worker_settings import WorkerSettings


class BotSettingsRepositoryInterface(ABC):
    @abstractmethod
    async def get_active_bot_settings(self) -> list[WorkerSettings]:
        pass
