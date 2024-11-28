from dataclasses import dataclass

from abstractions.repositories.EventsRepositoryInterface import EventsRepositoryInterface
from abstractions.usecases.BrokerEventsUseCaseInterface import BrokerEventsUseCaseInterface
from domain.events.broker import BaseEvent


@dataclass
class BrokerEventsUseCase(BrokerEventsUseCaseInterface):
    event_repository: EventsRepositoryInterface

    async def publish(self, event: BaseEvent):
        await self.event_repository.publish(event)
