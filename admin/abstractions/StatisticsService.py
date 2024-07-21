from abc import abstractmethod, ABC

from domain.statistics import StatisticsResponse


class StatisticsService(ABC):
    @abstractmethod
    async def get_statistics(self) -> StatisticsResponse:
        pass
