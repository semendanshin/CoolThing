from abc import abstractmethod, ABC
from dataclasses import dataclass

from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from domain.schemas.bots import ManagerBotOverview, ParserBotOverview, ManagerBotDetails, ParserBotDetails


@dataclass
class BotsUseCaseInterface(ABC):
    @abstractmethod
    async def get_bot(self, bot_username: str) -> ManagerBotDetails | ParserBotDetails:
        ...

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
