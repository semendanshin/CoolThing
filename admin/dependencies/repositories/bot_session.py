from typing import Callable

from abstractions.repositories.TelegramSessionRepositoryInterface import TelegramSessionRepositoryInterface
from infrastructure.repositories.PyrogramTelegramSessionRepository import PyrogramTelegramSessionRepository


def get_bots_sessions_repository() -> Callable[[], TelegramSessionRepositoryInterface]:
    repo = PyrogramTelegramSessionRepository()

    def _inner():
        return repo

    return _inner
