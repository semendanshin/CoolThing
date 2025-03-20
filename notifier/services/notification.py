import logging
from dataclasses import dataclass
from datetime import datetime

from abstractions.services.event_serializer import EventSerializerInterface
from abstractions.services.notifications import NotificationsServiceInterface
from abstractions.services.telegram.notificator import NotificatorInterface
from domain.events import Event
from domain.notifications import Notification

logger = logging.getLogger(__name__)


@dataclass
class NotificationsService(NotificationsServiceInterface):
    admins: list[int]
    notificator: NotificatorInterface
    event_serializer: EventSerializerInterface

    async def send_notification(self, event: Event):
        for admin in self.admins:
            message = await self.event_serializer.get_event_string(event)
            notification = Notification(
                event=event,
                text=message,
                send_to=admin
            )
            await self.notificator.send(
                notification=notification,
            )
            notification.sent_at = datetime.now()
            # todo: log notification sending with complete info (probably to db)
            logger.info(f'Notification sent, {notification}')
