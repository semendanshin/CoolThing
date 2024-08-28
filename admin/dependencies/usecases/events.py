from abstractions.usecases.EventsUseCaseInterface import EventsUseCaseInterface
from dependencies.repositories.events import get_event_repository
from usecases.EventsUseCase import EventsUseCase


def get_events_use_case() -> EventsUseCaseInterface:
    return EventsUseCase(
        event_repository=get_event_repository(),
    )
