from abstractions.usecases import BotsUseCaseInterface
from dependencies.repositories.campaign import get_campaign_repository
from dependencies.repositories.chats import get_chats_repository
from dependencies.repositories.gpt import get_gpt_repository
from dependencies.repositories.workers import get_workers_repository
from usecases.BotsUseCase import BotsUseCase
from usecases.mocks.MockBotsUseCase import MockBotsUseCase


def get_bots_usecase() -> BotsUseCaseInterface:
    return BotsUseCase(
        workers_repo=get_workers_repository(),
    )
