from dataclasses import dataclass

from abstractions.repositories.EventsRepositoryInterface import EventsRepositoryInterface
from abstractions.usecases.EventsUseCaseInterface import EventsUseCaseInterface
from domain.events import BaseEvent


@dataclass
class EventsUseCase(EventsUseCaseInterface):
    event_repository: EventsRepositoryInterface

    async def publish(self, event: BaseEvent):
        await self.event_repository.publish(event)
