from abc import ABC, abstractmethod

from domain.events.broker import BaseEvent


class BrokerEventsUseCaseInterface(ABC):
    @abstractmethod
    async def publish(self, broker_event: BaseEvent):
        ...
