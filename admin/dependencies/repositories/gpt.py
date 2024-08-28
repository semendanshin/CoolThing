from abstractions.repositories.GptSettingsRepositoryInterface import GptSettingsRepositoryInterface
from infrastructure.repositories.sqlalchemy.GptSettingsRepository import GPTRepository
from . import get_session_maker


def get_gpt_repository() -> GptSettingsRepositoryInterface:
    return GPTRepository(
        session_maker=get_session_maker(),
    )
