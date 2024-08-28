from abstractions.repositories.EventsRepositoryInterface import EventsRepositoryInterface
from config import settings
from infrastructure.mq import RabbitMQEventsRepository


def get_event_repository() -> EventsRepositoryInterface:
    return RabbitMQEventsRepository(
        url=settings.mq.url,
    )
