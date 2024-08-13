from abc import abstractmethod, ABC

from domain.schemas.statistics import StatisticsResponse


class StatisticsUseCaseInterface(ABC):
    @abstractmethod
    async def get_statistics(self) -> StatisticsResponse:
        pass
