from abc import ABC, abstractmethod

from domain.events import Event


class NotificationsServiceInterface(ABC):
    @abstractmethod
    async def send_notification(self, event: Event) -> None:
        ...
