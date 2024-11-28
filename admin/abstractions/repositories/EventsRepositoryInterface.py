from abc import abstractmethod, ABC

from domain.events.broker import BaseEvent


class EventsRepositoryInterface(ABC):
    @abstractmethod
    async def publish(self, event: BaseEvent):
        ...
