from abstractions.usecases.ChatsUseCaseInterface import ChatsUseCaseInterface
from usecases.mocks.MockChatsUseCase import MockChatsUseCase


def get_chats_service() -> ChatsUseCaseInterface:
    return MockChatsUseCase()
