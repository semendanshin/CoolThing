from abc import ABC, abstractmethod

from domain.events.system import BaseSystemEvent


class SystemEventsUseCaseInterface(ABC):
    @abstractmethod
    async def publish(self, system_event: BaseSystemEvent):
        ...
