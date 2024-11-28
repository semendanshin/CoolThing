from abc import ABC, abstractmethod

from domain.events import Event


class EventSerializerInterface(ABC):
    @abstractmethod
    async def get_event_string(self, event: Event) -> str:
        ...
