from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from dependencies.repositories.active_script_process import get_active_script_process_repository
from dependencies.repositories.scripts import get_scripts_repository, get_script_for_campaign_repository
from dependencies.usecases.events import get_events_use_case
from usecases.ScriptsUseCase import ScriptsUseCase


def get_scripts_use_case() -> ScriptsUseCaseInterface:
    return ScriptsUseCase(
        scripts_repository=get_scripts_repository(),
        scripts_for_campaign_repository=get_script_for_campaign_repository(),
        events_use_case=get_events_use_case(),
        script_process_repository=get_active_script_process_repository(),
    )
