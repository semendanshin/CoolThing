import logging
from dataclasses import dataclass

from httpx import AsyncClient

from abstractions.usecases.SystemEventsUseCaseInterface import SystemEventsUseCaseInterface
from domain.events.system import BaseSystemEvent

logger = logging.getLogger(__name__)


@dataclass
class SystemEventsUseCase(SystemEventsUseCaseInterface):
    base_url: str = 'http://notifier:8080'

    async def publish(self, system_event: BaseSystemEvent):
        with AsyncClient(base_url=self.base_url) as client:  # type: AsyncClient
            await client.post(
                url='/events',
                json=system_event.model_dump(),
            )
