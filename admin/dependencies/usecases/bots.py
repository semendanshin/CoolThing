from abstractions.usecases import BotsUseCaseInterface
from dependencies.repositories.bot_session import get_bots_sessions_repository
from dependencies.repositories.scripts import get_script_for_campaign_repository
from dependencies.repositories.workers import get_workers_repository
from usecases.BotsUseCase import BotsUseCase

session_repo_maker = get_bots_sessions_repository()


def get_bots_usecase() -> BotsUseCaseInterface:
    return BotsUseCase(
        workers_repo=get_workers_repository(),
        session_repo=session_repo_maker(),
        active_scripts_repo=get_script_for_campaign_repository(),
    )
