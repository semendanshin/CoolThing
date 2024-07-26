from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from . import get_session_maker
from infrastructure.repositories.ChatsRepository import ChatsRepository


def get_chats_repository() -> ChatsRepositoryInterface:
    return ChatsRepository(
        session_maker=get_session_maker(),
    )