from abc import abstractmethod, ABC

from domain.bots import ManagerBotOverview, ParserBotOverview, ManagerBotDetails, ParserBotDetails


class AbstractBotsService(ABC):
    @abstractmethod
    async def get_manager_bots(self) -> list[ManagerBotOverview]:
        ...

    @abstractmethod
    async def get_parser_bots(self) -> list[ParserBotOverview]:
        ...

    @abstractmethod
    async def connect_bot_by_code(self, code: str) -> bool:
        ...

    @abstractmethod
    async def connect_bot_by_password(self, password: str) -> bool:
        ...

    @abstractmethod
    async def get_bot(self, bot_username: str) -> ManagerBotDetails | ParserBotDetails:
        ...
