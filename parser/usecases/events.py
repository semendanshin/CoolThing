from abc import ABC
from dataclasses import dataclass

from domain.baseevent import BaseEvent


class EventRepository(ABC):
    async def publish(self, event: BaseEvent):
        pass


@dataclass
class EventUseCases:
    event_repository: EventRepository

    async def publish(self, event: BaseEvent):
        await self.event_repository.publish(event)
