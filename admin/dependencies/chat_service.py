from abstractions.AbstractChatsService import AbstractChatsService
from infrastructure.MockChatsService import MockChatsService


def get_chats_service() -> AbstractChatsService:
    return MockChatsService(

    )