from abstractions.usecases.BrokerEventsUseCaseInterface import BrokerEventsUseCaseInterface
from dependencies.repositories.events import get_event_repository
from usecases.EventsUseCase import BrokerEventsUseCase


def get_events_use_case() -> BrokerEventsUseCaseInterface:
    return BrokerEventsUseCase(
        event_repository=get_event_repository(),
    )
