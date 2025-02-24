from abstractions.service.active_script_process import ActiveScriptProcessServiceInterface
from dependencies.repositories.active_script_process import get_active_script_process_repository
from dependencies.scheduler import get_scheduler
from dependencies.services.campaign import get_campaign_service
from dependencies.repositories.script import get_script_repository
from dependencies.repositories.script_for_campaign import get_sfc_repository
from services.active_script import ActiveScriptProcessService
from settings import settings

_service: ActiveScriptProcessServiceInterface | None = None


def get_active_script_process_service() -> ActiveScriptProcessServiceInterface:
    global _service

    if not _service:
        _service = ActiveScriptProcessService(
                process_repository=get_active_script_process_repository(),
                campaign_service=get_campaign_service(),
                script_repository=get_script_repository(),
                sfc_repository=get_sfc_repository(),
                scheduler=get_scheduler(),
                decision_delay=settings.process.decision_delay,
            )

    return _service
