from typing import Callable

from abstractions.repositories.TelegramSessionRepositoryInterface import TelegramSessionRepositoryInterface
from infrastructure.repositories.telegram.telethon import TelethonTelegramSessionRepository


def get_bots_sessions_repository() -> Callable[[], TelegramSessionRepositoryInterface]:
    # repo = PyrogramTelegramSessionRepository()
    repo = TelethonTelegramSessionRepository()

    def _inner():
        return repo

    return _inner
