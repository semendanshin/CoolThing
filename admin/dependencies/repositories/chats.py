from abstractions.repositories.ChatsRepositoryInterface import ChatsRepositoryInterface
from infrastructure.repositories.ChatsRepository import ChatsRepository
from . import get_session_maker


def get_chats_repository() -> ChatsRepositoryInterface:
    return ChatsRepository(
        session_maker=get_session_maker(),
    )
