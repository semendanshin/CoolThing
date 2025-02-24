from abstractions.services.event_serializer import EventSerializerInterface
from dependencies.repositories.scripts import get_script_for_campaign_repository
from dependencies.services.workers import get_bots_service
from services.event_serializer import EventSerializer


def get_event_serializer() -> EventSerializerInterface:
    return EventSerializer(
        workers=get_bots_service(),
        active_scripts=get_script_for_campaign_repository(),
    )
