from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models import ScriptForCampaign


class ScriptsForCampaignRepositoryInterface(
    CRUDRepositoryInterface[
        ScriptForCampaign, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ABC,
):
    @abstractmethod
    async def stop_active_script(self, sfc_id: str) -> bool:
        ...
