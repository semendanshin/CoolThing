from abc import ABC, abstractmethod

from domain.events import BaseEvent


class EventsUseCaseInterface(ABC):
    @abstractmethod
    async def publish(self, event: BaseEvent):
        ...
