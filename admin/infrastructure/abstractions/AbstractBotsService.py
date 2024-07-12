from abc import abstractmethod, ABC

from domain.bots import BotOverview


class AbstractBotsService(ABC):
    @abstractmethod
    async def get_bots(self) -> list[BotOverview]:
        ...

    @abstractmethod
    async def connect_bot_by_code(self, code: str) -> bool:
        ...

    @abstractmethod
    async def connect_bot_by_password(self, password: str) -> bool:
        ...
