from typing import Callable

from abstractions.repositories.TelegramSessionRepositoryInterface import TelegramSessionRepositoryInterface
from infrastructure.repositories.PyrogramTelegramSessionRepository import PyrogramTelegramSessionRepository
from infrastructure.repositories.TelethonTelegramSessionRepository import TelethonTelegramSessionRepository


def get_bots_sessions_repository() -> Callable[[], TelegramSessionRepositoryInterface]:
    # repo = PyrogramTelegramSessionRepository()
    repo = TelethonTelegramSessionRepository()

    def _inner():
        return repo

    return _inner
