from abstractions.usecases.MessagesUseCaseInterface import MessagesUseCaseInterface
from dependencies.repositories.chats import get_chats_repository
from dependencies.repositories.messages import get_messages_repository
from dependencies.repositories.telegram_messages import get_telegram_messages_repository
from dependencies.repositories.uow import get_uow
from dependencies.repositories.workers import get_workers_repository
from usecases.MessagesUseCase import MessagesUseCase


def get_messages_service() -> MessagesUseCaseInterface:
    return MessagesUseCase(
        messages_repository=get_messages_repository(),
        chats_repository=get_chats_repository(),
        workers_repository=get_workers_repository(),
        telegram_messages_repository=get_telegram_messages_repository(),
        uow=get_uow(),
    )
