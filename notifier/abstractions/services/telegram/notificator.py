from abc import ABC, abstractmethod

from domain.notifications import Notification


class NotificatorInterface(ABC):
    @abstractmethod
    async def send(self, notification: Notification) -> Notification:
        ...

