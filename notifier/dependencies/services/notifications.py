from abstractions.services.notifications import NotificationsServiceInterface
from dependencies.services.event_serializer import get_event_serializer
from dependencies.services.telegram.notificator import get_notificator
from services.notification import NotificationsService
from settings import settings


def get_notification_service() -> NotificationsServiceInterface:
    return NotificationsService(
        admins=settings.bot.admins,
        notificator=get_notificator(),
        event_serializer=get_event_serializer(),
    )
