from abstractions.usecases.ChatsUseCaseInterface import ChatsUseCaseInterface
from dependencies.repositories.chats import get_chats_repository
from dependencies.repositories.uow import get_uow
from usecases.ChatsUseCase import ChatsUseCase


def get_chats_service() -> ChatsUseCaseInterface:
    return ChatsUseCase(
        repository=get_chats_repository(),
    )
