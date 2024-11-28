from abc import ABC

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models import ScriptForCampaign


class ScriptsForCampaignRepositoryInterface(
    CRUDRepositoryInterface[
        ScriptForCampaign, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ABC,
):
    ...
