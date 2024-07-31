from abstractions.usecases.ChatsUseCaseInterface import ChatsUseCaseInterface
from dependencies.repositories.chats import get_chats_repository
from usecases.ChatsUseCase import ChatsUseCase


def get_chats_service() -> ChatsUseCaseInterface:
    # return MockChatsUseCase()
    return ChatsUseCase(
        repository=get_chats_repository(),
    )
