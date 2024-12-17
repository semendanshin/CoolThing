from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models.script import ScriptForCampaign


class ScriptsForCampaignRepositoryInterface(
    CRUDRepositoryInterface[
        ScriptForCampaign, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ABC,
):
    ...
