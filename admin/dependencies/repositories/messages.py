from abstractions.repositories.MessagesRepositoryInterface import MessagesRepositoryInterface
from dependencies.repositories import get_session_maker
from infrastructure.repositories.MessagesRepository import MessagesRepository


def get_messages_repository() -> MessagesRepositoryInterface:
    return MessagesRepository(
        session_maker=get_session_maker(),
    )
