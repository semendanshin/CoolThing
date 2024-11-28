from abstractions.services.bots import BotsServiceInterface
from dependencies.repositories.workers import get_workers_repository
from services.bots import BotsService


def get_bots_service() -> BotsServiceInterface:
    return BotsService(
        workers=get_workers_repository(),
    )
